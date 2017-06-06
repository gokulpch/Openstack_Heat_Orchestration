# HEAT-OpenStack
Heat Orchestration Templates for Contrail/OpenContrail

![alt text](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/OpenStack%C2%AE_Logo_2016.svg/1280px-OpenStack%C2%AE_Logo_2016.svg.png)

#### /heat-templates

Heat template files are available here

#### /heat-env

env files to execute the template files are here

#### /autoscaling-heat

Heat templates to execute autoscaling tasks are here

#### /python-contrail-automation

Scripts using VNC api to automate creation of contrail-objects are here


## Using Openstack-Heat

### Terminology

**Stack**: In Heat parlance, a stack is the collection of objects—or resources—that will be created by Heat. This might include instances (VMs), networks, subnets, routers, ports, router interfaces, security groups, security group rules, auto-scaling rules, etc.

**Template**: Heat uses the idea of a template to define a stack. If you wanted to have a stack that created two instances connected by a private network, then your template would contain the definitions for two instances, a network, a subnet, and two network ports. Since templates are central to how Heat operates, I’ll show you examples of templates in this post.

**Parameters**: A Heat template has three major sections, and one of those sections defines the template’s parameters. These are tidbits of information—like a specific image ID, or a particular network ID—that are passed to the Heat template by the user. This allows users to create more generic templates that could potentially use different resources.

**Resources**: Resources are the specific objects that Heat will create and/or modify as part of its operation, and the second of the three major sections in a Heat template.

**Output**: The third and last major section of a Heat template is the output, which is information that is passed to the user, either via OpenStack Dashboard or via the heat stack-list and heat stack-show commands.

**HOT**: Short for Heat Orchestration Template, HOT is one of two template formats used by Heat. HOT is not backwards-compatible with AWS CloudFormation templates and can only be used with OpenStack. Templates in HOT format are typically—but not necessarily required to be—expressed as YAML (more information on YAML here).

##### https://github.com/openstack/heat


### Usage

**Create a Stack**

```
heat stack-create -e <.env> -f <.yaml> <stack-name>
example: heat stack-create -e create_vm.env -f create_vm.yaml vm-stack

```

**Check the status of the stack**

```
heat stack-show <stackname>

```

**List Active Stacks**

```
heat stack-list

```

**Delete a stack**

```
heat stack-delete <id> 

```
**CLI Reference**

##### https://docs.openstack.org/cli-reference/heat.html
