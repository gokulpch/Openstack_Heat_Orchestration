# RUN 

#### Heat Single Instance Autoscaling

[single_autoscale_env.yaml](https://github.com/savithruml/HOT-OpenStack/blob/master/autoscaling/single_autoscale_env.yaml) depends > [single_instance_scale.yaml](https://github.com/savithruml/HOT-OpenStack/blob/master/autoscaling/single_instance_scale.yaml)

`# heat stack-create <stack-name> -f single_autoscale.yaml -e single_autoscale_env.yaml`

#### Contrail SI Scaling

[contrail_si_autoscale.yaml](https://github.com/savithruml/HOT-OpenStack/blob/master/autoscaling/contrail_si_autoscale.yaml) depends > [contrail_si_scale.yaml](https://github.com/savithruml/HOT-OpenStack/blob/master/autoscaling/contrail_si_scale.yaml)

`# heat stack-create <stack-name> -f contrail_si_autoscale.yaml -e contrail_si_autoscale.env`



