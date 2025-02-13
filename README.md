# ARCLab-CCCatheter

## Dependencies

- **Blender** (Modify the path to the Blender executable in `scripts/path_settings.py` if necessary)  

### Python Packages:
- `numpy`
- `opencv-python`
- `matplotlib`
- `tqdm`
- `shapely`
- `scikit-image`
- `torch`, `torchvision`, `torchaudio`
- `bpy`
- `mathutils==2.81.2`

### Special Notes for Windows Users:
For Windows, the following versions have been tested to work:
- **Python**: `3.7`
- **CUDA**: `12.1` (for PyTorch GPU acceleration)
- **Visual Studio Build Tools**: `2019 (16.11.36)`

Ensure that the correct versions are installed to avoid compatibility issues.

## Routine of Operation
1. Modify `scripts/path_settings.py` and other directory paths in other scripts
2. Select desired experiment in `scripts\experiment_setup.py`
3. Choose the correct camera settings in `scripts\experiment_setup.py`
4. Setup the experiment executors and run
5. Use the experiment interpretors to visualize the results

If you want Blender to render curves in the background without interrupting script execution, 
add the '--background' tag to subprocess.run([]) inside scripts/bezier_set.py

## File Descriptions

### Reconstruction

#### Main Files
- **scripts\reconstruction_single.py**
  - Sample execution script that run a single shape reconstruction process and visualize the results. 

- **scripts\catheter_reconstruction\reconst_3_loss.py**
  - File that encapsulates the core optimization algorithm with 3 loss functions, which can be invoked by the control pipeline. 

- **scripts\catheter_reconstruction\reconst_2_loss.py**
  - File that encapsulates the core optimization algorithm with 2 loss functions. 


#### Testing Files
- **scripts\test_diff_render_catheter_v2\test_contour.ipynb**
  - Contains tests for reference contour of the catheter.

- **scripts\test_diff_render_catheter_v2\test_centerline.ipynb**
  - Contains tests for reference centerline of the catheter.
  
- **scripts\test_diff_render_catheter_v2\test_read_gt&cam_proj.ipynb**
  - Contains tests for the reading of ground truth and projected centerline and contour of the catheter.

- **scripts\test_diff_render_catheter_v2\test_construction_bezier.ipynb**
  - Contains tests for the process of generating projected centerline and contour of the catheter.
  
- **scripts\test_diff_render_catheter_v2\test_process.py**
  - A comprehensive test file. For a ground truth image and a initial guess, test the reading of ground truth data, image processing, projected and reference centerline and contour, 3D visualization.

- **scripts\catheter_reconstruction\test_catheter_motion3.ipynb**
  - File used to test the accuracy of inverse solution of the motion model used in reconstruction.

- **scripts\catheter_reconstruction\test_past_frame.ipynb**
  - File used to test the accuracy of the projection of catheter in the past frames.

- **scripts\catheter_reconstruction\test_recon_cam.py**
  - Test the camera projection in the catheter shape reconstruction pipeline.

- **scripts\catheter_reconstruction\test_recons_new_v3.py**
  - This script is the new version of the catheter reconstruction algorithm. 

- **scripts\catheter_reconstruction\reconstructionOptimizer_main.py**
  - Integrated code for the new version of the catheter reconstruction algorithm, which enables large-scale testing.
  
- **scripts\test_diff_render_catheter_v2\test_recon_old2.py**
  - This script is the old version of the catheter reconstruction algorithm. It is provided for comparison and testing purposes.

- **scripts\test_diff_render_catheter_v2\recon_old_main.py**
  - Integrated code for the old version of the catheter reconstruction algorithm, which enables large-scale testing.

#### Utils
- **scripts\catheter_reconstruction\plot_3d_bezier.py**
  - This script is used for plotting 3D Bezier curves to visualize the results of the catheter reconstruction.

- **scripts\catheter_reconstruction\read_data.py**
  - This script is used for reading and visualizing the data saved during the reconstruction process.

- **scripts\bezier_set.py**
  - Script that call `blender_files\render_bezier_blender.py` to generate catheter images using Blender based on the specified catheter parameters.

- **blender_files\render_bezier_blender.py**
  - Script that call Blender to perform the rendering of the catheter images. It specifies the parameters of the rendering.

- **scripts\catheter_reconstruction\plot_optimization_loss.ipynb**
  - Plot the loss of the optimization process.

- **scripts\test_diff_render_catheter_v2\gt_generation.ipynb**
  - This Jupyter notebook is used for generating ground truth data.

### Control

#### Main Files

- **scripts\simulation_experiment.py**
  - Main pipeline of control simulation.

- **scripts\cc_catheter.py**
  - Define the class that represents the catheter in simulation.

#### Experiment Execution Files

- **scripts\experiment_execution.py**
  - Generate dataset and execute the target reaching experiment for all targets in the dataset.

- **scripts\experiment_execution_single.py**
  - Execute the target reaching experiment on designated target points in the dataset.

- **scripts\castnet_experiments.py**
  - Execute the image space target reaching experiment.

- **scripts\castnet_experiments_single.py**
  - Execute the image space target reaching experiment for sepecific target points.

- **scripts\waypoint_guidance_experiments.py**
  - Execute the waypoint tracking experiment.


#### Experiment Results Interpretation Files

- **scripts\convergence_test_interpreter.ipynb**
  - Analyze and visualize the results of the target reaching experiment.

- **scripts\result_interpreter_casnet.ipynb**
  - Visualize the result of the image space target reaching experiment.

- **scripts\result_interpreter_waypoint.py**
  - Visualize results of the waypoint tracking experiment.


#### Testing Files

- **scripts\test_data_generation.ipynb**
  - Script for testing the generation of targets of the experiment and their visualization.

- **scripts\catheter_reconstruction\cc_bezier.py**
  - Script for visualizing the conversion of constant curvature curve to bezier curve.

- **scripts\test_plot_loss.ipynb**
  - Test the method to plot control loss in the simulation pipeline (simulation_experiment.py).

- **scripts\catheter_reconstruction\test_noise_generation.py**
  - Test the noise generation method for conversion from constant curvature model to bezier curve.

- **scripts\catheter_reconstruction\catheter_workspace.py**
  - Plot the workspace of the catheter for a given set of parameters.

- **scripts\catheter_reconstruction\test_3d_to_2d.ipynb**
  - Test the camera projection method in the control simulation pipeline.

- **scripts\test_diff_render_catheter_v2\test_camera_view.py**
  - Script that test the camera projection calculation (matching between numerical computation and Blender rendering).

#### Utils

- **scripts\contour_generation.ipynb**
  - Generate contour images for waypoint guidance experiment.

- **scripts\scripts\plot_2d_shape_control.ipynb**
  - Visualize target bezier curve for convergence test of 2D shape loss.

- **scripts\target_data_generation.py**
  - Generate targets for the simulation experiments for catheter control. Extracted from scripts\experiment_execution.py.

- **scripts\target_data_modify.ipynb**
  - Modify certain data points in the dataset for target reaching experiment.

- **scripts\catheter_reconstruction\plot_3d_bezier.py**
  - Plot 3D Bezier curve (with surface). Shape reconstruction.

- **scripts\catheter_reconstruction\plot_3d_bezier_control.py**
  - Plot 3D Bezier curve (with surface). Control experiment.

- **scripts\plot_convergence_test.ipynb**
  - Plot the error curves of the target reaching experiment (version 1).

- **scripts\catheter_reconstruction\plot_control_loss_curve.ipynb**
  - Plot the error curves of the target reaching experiment (version 2).

- **scripts\catheter_reconstruction\plot_tube.py**
  - Plot 3-D schematic diagram of the Bezier curve (in paper).

- **scripts\catheter_reconstruction\plot_2d_bezier_control.ipynb**
  - Plot the schematic diagram of the 2-D control process (in paper).

- **scripts\jacobian_derivation.ipynb**
  - Script for mathematical derivation. Calculate the jacobian of T matrix.

- **scripts\test_motion_model.ipynb**
  - Script for validation of the constant curvature motion model. Validate that T @ p0 = T @ [0,0,0,1] + p0.

### Usage

- **blender_files\render_bezier_blender.py**
  - This script configures render settings, including materials, camera and lighting, and then invokes Blender to render the Bezier curve based on the specified curve parameters.

- **scripts\path_settings.py**
  - The file contains the commonly used file and directory paths for this project.

- **scripts\camera_settings.py**
  - Define camera settings (intrinsic and extrinsic parameters) for the simulation experiments. Shoule be consistent with the camera settings in Blender.

- **scripts\experiment_setup.py**
  - This file defines various experiments.

## Full Path Tree
```bash
ARCLab-CCCatheter
│
├──blender_files
│  ├──render_bezier_blender.py          ## Blender script used in main pipeline
│  ├──render_bezier.blend               ## (Optional) for visualization
│  └──render_bezier.blend1              ## (Optional) goes with .blend
├──data
│  ├──bezier_specs                      ## temporary storage to be used during execution of main pipeline
│  ├──contour_images                    ## data of contour images
│  ├──rendered_images                   ## for visualizing rendered images
│  ├──rendered_videos                   ## for visualizing rendered videos
│  └──target_parameters                 ## data generated for convergence experiment
├──results                              ## results of experiments and tables and figures produced by result interpreters
└──scripts
   ├──reconstruction_scripts            ## Fei's reconstruction algorithms
   │  ├──reconst_sim_opt2pts.py
   │  └──reconst_sim_opt3pts.py 
   ├──bezier_interspace_transforms.py   ## calculations for interspace transforms 
   ├──bezier_set.py                     ## Calls Blender script to render Bezier curves
   ├──camera_settings.py
   ├──castnet_experiments.py            ## executor for heatmap experiment
   ├──cc_catheter.py                    ## basic catheter class
   ├──contour_tracer.py                 ## trace contour for shape on an image
   ├──convert_camera_settings.py
   ├──data_generation.py                ## data generator for convergence experiment
   ├──experiment_execution.py           ## executor for convergence experiment
   ├──experiment_setup.py               ## parameter settings for all methods
   ├──identifier_conversions.py         ## conversions between method names, identifiers, and indices
   ├──path_settings.py
   ├──result_interpreter_castnet.py     ## result interpreter for heatmap experiment
   ├──result_interpreter_general.py     ## result interpreter for convergence experiment
   ├──result_interpreter_waypoint.py    ## result interpreter for waypoint experiment
   ├──simulation_experiment.py          ## wrap basic catheter class in a pipeline
   ├──temp_image_modifier.py            ## (tangent)
   ├──transforms.py                     ## calculations for unispace transforms (these are also used by interspace transforms)
   ├──waypoint_guidance_experiments.py  ## executor for waypoint experiment
   └──write_video_from_img.py           ## (tangent) 
```

## Updated Full Path Tree (11/21/23)
```bash 
├── README.md
├── blender_files
│   ├── render_bezier.blend
│   ├── render_bezier.blend1
│   ├── render_bezier_blender.py                         ## Blender parser to generate inputted info (i.e., curve)
│   ├── rod_original (copy).blend
│   ├── rod_original (copy).blend1
│   ├── rod_original.blend
│   └── rod_original.blend1
├── file_structure.txt
├── results
│   └── table_1_p3d.csv
└── scripts
    ├── __pycache__
    │   ├── bezier_set.cpython-310.pyc
    │   ├── bezier_set.cpython-38.pyc
    │   ├── camera_settings.cpython-310.pyc
    │   ├── camera_settings.cpython-38.pyc
    │   ├── path_settings.cpython-310.pyc
    │   └── path_settings.cpython-38.pyc
    ├── bezier_interspace_transforms.py
    ├── bezier_set.py                                    ## Takes in bezier curve info and renders it in Blender
    ├── cam_test.py
    ├── camera_settings.py
    ├── castnet_experiments.py
    ├── cc_catheter.py
    ├── contour_tracer.py
    ├── convert_camera_settings.py
    ├── data_generation.py
    ├── diff_render
    │   ├── BKups
    │   │   └── diff_render_2pts_BKUP.py
    │   ├── __pycache__
    │   │   ├── bezier_set.cpython-310.pyc
    │   │   ├── blender_catheter.cpython-310.pyc
    │   │   ├── blender_catheter.cpython-38.pyc
    │   │   ├── build_diff_model.cpython-38.pyc
    │   │   ├── construction_bezier.cpython-310.pyc
    │   │   ├── construction_bezier.cpython-38.pyc
    │   │   ├── diff_render_catheter.cpython-310.pyc
    │   │   ├── diff_render_catheter.cpython-38.pyc
    │   │   ├── loss_define.cpython-310.pyc
    │   │   └── loss_define.cpython-38.pyc
    │   ├── blender_catheter.py
    │   ├── blender_imgs
    │   │   ├── cylinder_primitve.mtl
    │   │   ├── cylinder_primitve.obj
    │   │   ├── diff_render_1.mtl
    │   │   ├── diff_render_1.npy
    │   │   ├── diff_render_1.obj
    │   │   ├── diff_render_1.png
    │   │   ├── diff_render_2.npy
    │   │   └── diff_render_2.png
    │   ├── build_diff_model.py
    │   ├── camera_position_optimization_with_differentiable_rendering.ipynb
    │   ├── construction_bezier.py
    │   ├── cylinder.mat
    │   ├── cylinder_primitive.csv
    │   ├── cylinder_primitive.npy
    │   ├── diff_open_blender.py
    │   ├── diff_optimize_2pts.py
    │   ├── diff_optimize_2pts_ok.py
    │   ├── diff_render_catheter.py
    │   ├── get-pip.py
    │   ├── install_torch3d.py
    │   ├── loss_define.py
    │   ├── projectCurve.ipynb
    │   ├── test_code.m
    │   ├── test_cyl_constr.py
    │   ├── test_diff_render.ipynb
    │   ├── test_generate_primitive.ipynb
    │   ├── test_torch3d_rendering.ipynb
    │   └── test_torch3d_rendering_CLEAN.ipynb
    ├── experiment_execution.py
    ├── experiment_setup.py
    ├── hough_bezier.py
    ├── identifier_conversions.py
    ├── path_settings.py
    ├── postprocessing.py
    ├── real_robot_experiment.py
    ├── real_robot_experiment_executor.py
    ├── reconstruction_scripts
    │   ├── 05_DataAssociation-Clutter.py
    │   ├── 07_PDATutorial.py
    │   ├── PDA_test.py
    │   ├── reconst_sim_opt2pts.py
    │   ├── reconst_sim_opt2pts_PDA.py
    │   ├── reconst_sim_opt3pts.py
    │   └── usage.md
    ├── result_interpreter_castnet.py
    ├── result_interpreter_general.py
    ├── result_interpreter_waypoint.py
    ├── simulation_experiment.py
    ├── temp_image_modifier.py
    ├── test_diff_render_catheter               ## OG attempt at reconst                      
    │   └── ...
    ├── test_diff_render_catheter_v2            ## SRC Reconst code directory
    │   ├── blender_imgs
    │   │   ├── test_catheter_gt1.npy           ## Sample npy of blender catheter
    │   │   └── test_catheter_gt1.png           ## Sample png of blender catheter
    │   ├── important_imgs
    │   │   ├── render_59_tipBP-mean.jpg
    │   │   ├── render_59_tipBP-sum.jpg
    │   │   └── render_59_tiponly-mean.jpg
    │   ├── math_calcuations.py                 ## Extra file for math calculations
    │   ├── test_blender_catheter.py            ## Render bezier catheter in blender. Calls upon `scripts/bezier_set.py`
    │   ├── test_diff_render_catheter_v2.py     ## Unused
    │   ├── test_graph_random.py                ## Script to test and graph inter-pipeline plots/images
    │   ├── test_loss_define_v2.py              ## Loss functions for optimization algorithm
    │   ├── test_optimize_v2.py                 ## Main script for catheter reconstruction optimization
    │   ├── test_plot_2_curves.py               ## Same as `test_reconst_v2.py`, but can plot 2 curves in 3d space
    │   └── test_reconst_v2.py                  ## Script to generate 3d bezier catheter model & get 2d projection
    ├── transforms.py
    ├── waypoint_guidance_experiments.py
    └── write_video_from_img.py

```

## Logical Hierarchy
```bash
## Upper Level
├──result_interpreter_general.py
│  ├──identifier_conversions.py
│  └──experiment_execution.py
│     ├──data_generation.py
│     ├──experiment_setup.py
│     └──simulation_experiment.py
│
├──result_interpreter_castnet.py
│  ├──identifier_conversions.py
│  └──castnet_experiments.py
│     ├──experiment_setup.py
│     └──simulation_experiment.py
│  
└──result_interpreter_waypoint.py
   ├──identifier_conversions.py
   └──waypoint_guidance_experiments.py
      ├──contour_tracer.py
      ├──experiment_setup.py
      └──simulation_experiment.py

## Lower Level
simulation_experiment.py
├──reconst_sim_opt2pts.py
└──cc_catheter.py
   ├──transforms.py                  
   ├──bezier_interspace_transforms.py
   └──bezier_set.py  
      └──render_bezier_blender.py
```
