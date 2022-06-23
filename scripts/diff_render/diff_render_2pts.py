import sys

sys.path.append('..')

import os
import numpy as np

# import transforms
# import bezier_interspace_transforms
from bezier_set import BezierSet
import camera_settings

import torch

import open3d as o3d


class DiffRenderCatheter:

    def __init__(self):

        ## initialize camera parameters
        self.setCameraParams(camera_settings.a, camera_settings.b, camera_settings.center_x, camera_settings.center_y,
                             camera_settings.image_size_x, camera_settings.image_size_y, camera_settings.extrinsics,
                             camera_settings.intrinsics)

        ## initialize a catheter
        n_beziers = 1
        self.bezier_set = BezierSet(n_beziers)

        self.bezier_num_samples = 101
        self.bezier_surface_resolution = 50

        self.bezier_radius = 0.0015

    def setCameraParams(self, fx, fy, cx, cy, size_x, size_y, camera_extrinsics, camera_intrinsics):
        """
        Set intrinsic and extrinsic camera parameters

        Args:
            fx (float): horizontal direction focal length
            fy (float): vertical direction focal length
            cx (float): horizontal center of image
            cy (float): vertical center of image
            size_x (int): width of image
            size_y (int): height of image
            camera_extrinsics ((4, 4) numpy array): RT matrix 
            camera_intrinsics ((3, 3) numpy array): K matrix 
        """
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy
        self.size_x = size_x
        self.size_y = size_y
        self.cam_RT_H = camera_extrinsics
        self.cam_K = camera_intrinsics

        # camera E parameters
        cam_RT_H = torch.tensor([[1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
        invert_y = torch.tensor([[1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
        self.cam_RT_H = torch.matmul(invert_y, cam_RT_H)

    def getBezierCurve(self, para_gt, p_start):

        p_mid = para_gt[0:3]
        p_end = para_gt[3:6]
        p_c1 = 4 / 3 * p_mid - 1 / 3 * p_start
        p_c2 = 4 / 3 * p_mid - 1 / 3 * p_end
        # self.control_pts = torch.vstack((p_start, c2, p_end, c1))

        sample_list = torch.linspace(0, 1, self.bezier_num_samples)

        # Get positions and normals from samples along bezier curve
        self.bezier_pos = torch.zeros(self.bezier_num_samples, 3)
        self.bezier_der = torch.zeros(self.bezier_num_samples, 3)
        self.bezier_snd_der = torch.zeros(self.bezier_num_samples, 3)
        for i, s in enumerate(sample_list):
            self.bezier_pos[i, :] = (1 - s)**3 * p_start + 3 * s * (1 - s)**2 * \
                p_c1 + 3 * (1 - s) * s**2 * p_c2 + s**3 * p_end
            self.bezier_der[i, :] = -(1 - s)**2 * p_start + ((1 - s)**2 - 2 * s *
                                                             (1 - s)) * p_c1 + (-s**2 + 2 *
                                                                                (1 - s) * s) * p_c2 + s**2 * p_end
            self.bezier_snd_der[i, :] = 6 * (1 - s) * (p_c2 - 2 * p_c1 + p_start) + 6 * s * (p_end - 2 * p_c2 + p_c1)

        # Convert positions and normals to camera frame
        pos_bezier_H = torch.cat((self.bezier_pos, torch.ones(self.bezier_num_samples, 1)), dim=1)

        pos_bezier_cam_H = torch.transpose(torch.matmul(self.cam_RT_H, torch.transpose(pos_bezier_H, 0, 1)), 0, 1)
        self.pos_bezier_cam = pos_bezier_cam_H[1:, :-1]

        der_bezier_H = torch.cat((self.bezier_der, torch.zeros((self.bezier_num_samples, 1))), dim=1)
        der_bezier_cam_H = torch.transpose(torch.matmul(self.cam_RT_H, torch.transpose(der_bezier_H[1:, :], 0, 1)), 0,
                                           1)
        self.der_bezier_cam = der_bezier_cam_H[:, :-1]

    def getBezierTNB(self, bezier_pos, bezier_der, bezier_snd_der):

        bezier_der_n = torch.linalg.norm(bezier_der, ord=2, dim=1)
        self.bezier_tangent = bezier_der / torch.unsqueeze(bezier_der_n, dim=1)

        bezier_normal_numerator = torch.linalg.cross(bezier_der, torch.linalg.cross(bezier_snd_der, bezier_der))
        bezier_normal_numerator_n = torch.mul(
            bezier_der_n, torch.linalg.norm(torch.linalg.cross(bezier_snd_der, bezier_der), ord=2, dim=1))

        self.bezier_normal = bezier_normal_numerator / torch.unsqueeze(bezier_normal_numerator_n, dim=1)

        bezier_binormal_numerator = torch.linalg.cross(bezier_der, bezier_snd_der)
        bezier_binormal_numerator_n = torch.linalg.norm(bezier_binormal_numerator, ord=2, dim=1)

        self.bezier_binormal = bezier_binormal_numerator / torch.unsqueeze(bezier_binormal_numerator_n, dim=1)

    def getBezierSurface(self):

        self.bezier_surface = torch.zeros(self.bezier_num_samples, self.bezier_surface_resolution, 3)

        theta_list = torch.linspace(0.0, 2 * np.pi, self.bezier_surface_resolution)

        for i in range(self.bezier_num_samples):
            surface_vec = self.bezier_radius * (
                -torch.mul(self.bezier_normal[1, :], torch.unsqueeze(torch.cos(theta_list), dim=1)) +
                torch.mul(self.bezier_binormal[1, :], torch.unsqueeze(torch.sin(theta_list), dim=1)))

            self.bezier_surface[i, :, :] = self.bezier_pos[i, :] + surface_vec

    def createCylinderPrimitive(self):
        self.mesh_cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=1,
                                                                       height=10.0,
                                                                       resolution=self.bezier_surface_resolution,
                                                                       split=self.bezier_num_samples - 1,
                                                                       create_uv_map=False)
        self.mesh_cylinder.compute_vertex_normals()
        self.mesh_cylinder.paint_uniform_color([0.1, 0.9, 0.1])
        self.mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.6, origin=[0, 0, 0])

    def createOpen3DVisualizer(self):

        # Visualizer
        self.vis = o3d.visualization.VisualizerWithKeyCallback()
        self.vis.create_window()
        self.vis.register_key_callback(88, self.closeOpen3DVisualizer)
        self.vis.get_view_control().set_zoom(1.5)

        # o3d.visualization.draw_geometries([mesh_cylinder, mesh_frame])
        self.vis.add_geometry(self.mesh_cylinder)
        self.vis.add_geometry(self.mesh_frame)

    def updateOpen3DVisualizer(self):

        surface_vertices = torch.reshape(self.bezier_surface, (-1, 3))
        top_center_vertice = torch.unsqueeze(self.bezier_pos[0, :], dim=0)
        bot_center_vertice = torch.unsqueeze(self.bezier_pos[-1, :], dim=0)
        update_vertices = torch.cat((top_center_vertice, bot_center_vertice, surface_vertices), dim=0).detach().numpy()

        # self.mesh_cylinder.vertices = o3d.utility.Vector3dVector(update_vertices)

        # self.vis.update_geometry(self.mesh_cylinder)
        # self.vis.update_renderer()

        o3d.visualization.draw_geometries([self.mesh_cylinder])

        self.vis_view = o3d.visualization.ViewControl
        self.vis_view.camera_local_translate(0, 0, 0)

    def closeOpen3DVisualizer(vis):
        print('Closing visualizer!')


class BlenderRenderCatheter:

    def __init__(self):

        ## initialize a catheter
        n_beziers = 1
        self.bezier_set = BezierSet(n_beziers)

    def set_bezier_in_blender(self, para_gt, p_start):
        p_mid = para_gt[0:3]
        p_end = para_gt[3:6]

        # c = (p_mid - (p_start / 4) - (p_end / 4)) * 2
        c1 = 4 / 3 * p_mid - 1 / 3 * p_end
        c2 = 4 / 3 * p_mid - 1 / 3 * p_start

        self.bezier_set.enter_spec(p_start, p_end, c1, c2)

    def render_bezier_in_blender(self,
                                 curve_specs_path,
                                 img_save_path,
                                 target_specs_path=None,
                                 viewpoint_mode=1,
                                 transparent_mode=0):
        """
        Render Bezier curves according to the curve specs.

        Args:
            curve_specs_path (path string to npy file): curve specs is a (n, 3) numpy array where each
                row specifies the start point, middle control point, and end point of a Bezier curve
            img_save_path (path string to png file): path to save rendered image
            target_specs_path (path string to npy file): target specs is a (n, 3) numpy array where each
                row specifies the 3D position of a target point. If this path is set to None,
                target points will be not rendered
            viewpoint_mode (1 or 2): camera view of rendered image, 1 for endoscopic view, 2 for side view
            transparent_mode (0 or 1): whether to make the background transparent for the rendered image,
                0 for not transparent, 1 for transparent
        """
        if not self.bezier_set:
            print('[ERROR] [CCCatheter] self.bezier_set invalid. Run calculate_beziers_control_points() first')
            exit()

        self.bezier_set.print_specs()
        self.bezier_set.write_specs(curve_specs_path)
        self.bezier_set.render(img_save_path, target_specs_path, viewpoint_mode, transparent_mode)


if __name__ == '__main__':

    blender_catheter = BlenderRenderCatheter()

    para_gt = torch.tensor([0.02003904, 0.0016096, 0.10205799, 0.02489567, -0.04695673, 0.196168896], dtype=torch.float)
    p_start = torch.tensor([0.02, 0.002, 0.0])

    # case_naming = '/home/fei/ARCLab-CCCatheter/scripts/diff_render/blender_imgs/diff_render_1'
    # img_save_path = case_naming + '.png'
    # cc_specs_path = case_naming + '.npy'
    # target_specs_path = None
    # viewpoint_mode = 1
    # transparent_mode = 0

    # blender_catheter.set_bezier_in_blender(para_gt.detach().numpy(), p_start.detach().numpy())

    # blender_catheter.render_bezier_in_blender(cc_specs_path, img_save_path, target_specs_path, viewpoint_mode,
    #                                          transparent_mode)

    diff_catheter = DiffRenderCatheter()

    ## define a bezier curve
    diff_catheter.getBezierCurve(para_gt, p_start)

    ## get the bezier in TNB frame, in order to build a tube mesh
    diff_catheter.getBezierTNB(diff_catheter.bezier_pos, diff_catheter.bezier_der, diff_catheter.bezier_snd_der)

    ## get bezier surface mesh
    ## ref : https://mathworld.wolfram.com/Tube.html
    diff_catheter.getBezierSurface()

    diff_catheter.createCylinderPrimitive()
    # diff_catheter.createOpen3DVisualizer()
    diff_catheter.updateOpen3DVisualizer()
