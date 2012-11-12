from cogent.util.option_parsing import make_option

script_info = {}
script_info['brief_description'] = "An example of brief description"
script_info['script_description'] = "An example of script description"
script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
script_info['output_description'] = "Field not used"
script_info['required_options'] = [
	make_option('-i', '--input_fp', type="existing_path",
				help='An example of existing_path option'),
	make_option('-o', '--output_fp', type="new_path",
				help='An example of new_path option')
]
script_info['optional_options'] = [
	make_option('-c', '--choice_ex', type="choice", choices=['choice1','choice2','choice3'],
				help='An example of choice option'),
	make_option('-r', '--repeat_ex', type="existing_filepaths",
				help='An example of existing_filepaths option')
]
script_info['version'] = "1.4.0-dev"