cloud-formation-viz
===================

This tool is for creating visualizations of CloudFormation templates.

Installation:
```` bash
cd cloud-formation-viz
python -m venv .venv 
source .venv/bin/activate
python setup.py install
````

The help message can be printed with the following command:
```` bash
Usage: cfviz [OPTIONS] [INPUT] [OUTPUT]

  INPUT input filename [default: stdin]

  OUTPUT output filename [default: stdout]

Options:
  --unique-edges / --no-unique-edges
  --parameters / --no-parameters
  --outputs / --no-outputs
  --pseudo / --no-pseudo
  --globals / --no-globals
  --icons-path PATH
  --version                       Show the version and exit.
  --help                          Show this message and exit.
````

It outputs Graphviz dot files. It can be used like this where 
example.template is a json cloudformation template:
```` bash
cat example.template | cfviz | dot -Tsvg -oexample.svg
````

The following can also be used:
```` bash
cfviz example.yaml | dot -Tsvg -oexample.svg
cfviz example.yaml - | dot -Tsvg -oexample.svg
cfviz example.yaml example.dot
````

There are three dependencies of the `cfviz` Python (>=3.7) script. 
Required packages:
* [PyYaml](https://github.com/yaml/pyyaml)
* [cfn-flip](https://github.com/awslabs/aws-cfn-template-flip)
* [Click](https://click.palletsprojects.com)

You will also need to have [Graphviz](http://www.graphviz.org/) 
installed for the output to be any use.

The [samples](https://github.com/benbc/cloud-formation-viz/tree/master/samples) 
directory contains output of running the tool over the 
[aws-samples](http://aws.amazon.com/cloudformation/aws-cloudformation-templates/) 
provided by AWS.

To add icons to the output run the procedure in the icons/get-icons.sh file.
Note some of the references to resources on the AWS site might need to be 
updated as new icon sets are released.

 The following then can be used:
```` bash
cfviz --icons-path icons/ template.yaml - | dot -Tpng -otemplate.png
````