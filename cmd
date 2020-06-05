sudo docker run -ti -m 16GB --rm -v /media/antor/work1/projects/odm/datasets:/datasets opendronemap/odm --project-path /datasets project --dsm --orthophoto-resolution 1.7 --texturing-nadir-weight 32 --mesh-octree-depth 11 --dem-resolution 1.7 --orthophoto-cutline --ignore-gsd --pc-csv --pc-las --use-3dmesh --crop 3 --verbose





sudo docker run -ti -m 16GB --rm -v /media/antor/work1/projects/odm/datasets:/datasets opendronemap/odm --project-path /datasets project --dsm --orthophoto-resolution 5 --dem-resolution 5 --orthophoto-cutline --pc-csv --pc-las --crop 3 --verbose

