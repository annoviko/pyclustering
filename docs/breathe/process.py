
AUTOCFG_TEMPLATE = r"""
PROJECT_NAME     = "{project_name}"
OUTPUT_DIRECTORY = {output_dir}
GENERATE_LATEX   = NO
GENERATE_MAN     = NO
GENERATE_RTF     = NO
CASE_SENSE_NAMES = NO
INPUT            = {input}
ENABLE_PREPROCESSING = YES
QUIET            = YES
JAVADOC_AUTOBRIEF = YES
JAVADOC_AUTOBRIEF = NO
GENERATE_HTML = NO
GENERATE_XML = YES
ALIASES = "rst=\verbatim embed:rst"
ALIASES += "endrst=\endverbatim"
""".strip()

class ProjectData(object):
    "Simple handler for the files and project_info for each project"

    def __init__(self, auto_project_info, files):

        self.auto_project_info = auto_project_info
        self.files = files

class AutoDoxygenProcessHandle(object):

    def __init__(self, path_handler, run_process, write_file, project_info_factory):

        self.path_handler = path_handler
        self.run_process = run_process
        self.write_file = write_file
        self.project_info_factory = project_info_factory

    def generate_xml(self, app):

        project_files = {}

        # First collect together all the files which need to be doxygen processed for each project
        for project_name, file_structure in app.config.breathe_projects_source.items():

            folder = file_structure[0]
            contents = file_structure[1]

            auto_project_info = self.project_info_factory.create_auto_project_info(
                    project_name, folder)

            project_files[project_name] = ProjectData(auto_project_info, contents)

        # Iterate over the projects and generate doxygen xml output for the files for each one into
        # a directory in the Sphinx build area
        for project_name, data in project_files.items():

            project_path = self.process(data.auto_project_info, data.files)

            project_info = data.auto_project_info.create_project_info(project_path)

            self.project_info_factory.store_project_info_for_auto(project_name, project_info)

    def process(self, auto_project_info, files):

        name = auto_project_info.name()
        cfgfile = "%s.cfg" % name

        full_paths = map(lambda x: auto_project_info.abs_path_to_source_file(x), files)

        cfg = AUTOCFG_TEMPLATE.format(
            project_name=name,
            output_dir=name,
            input=" ".join(full_paths)
            )

        build_dir = self.path_handler.join(
            auto_project_info.build_dir(),
            "breathe",
            "doxygen"
            )

        self.write_file(build_dir, cfgfile, cfg)

        self.run_process(['doxygen', cfgfile], cwd=build_dir)

        return self.path_handler.join(build_dir, name, "xml")

