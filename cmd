sudo docker run -ti --rm -v /media/antor/work1/projects/odm/datasets:/datasets opendronemap/odm --project-path /datasets project --dsm --orthophoto-resolution 1.7 --texturing-nadir-weight 32 --mesh-octree-depth 11 --dem-resolution 1.7 --orthophoto-cutline --ignore-gsd --pc-csv --pc-las --use-3dmesh --crop

