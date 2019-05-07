from conans import ConanFile, CMake, tools
import os

class Jinja2cppConan(ConanFile):
    name = "jinja2cpp"
    license = "MIT"
    url = "https://github.com/Jinja2Cpp/Jinja2Cpp"
    description = "Jinja2 C++ (and for C++) almost full-conformance template engine implementation"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "git_upstream_url": "ANY"
    }
    default_options = "shared=False", "git_upstream_url=\"https://github.com/Jinja2Cpp/Jinja2Cpp\""
    generators = "cmake_find_package"
    requires = (
        "boost/1.70.0@conan/stable"
        # "variant-lite/1.1.0@Manu343726/testing",
        # "expected-lite/0.2.0@Manu343726/testing",
        # "value-ptr-lite/0.1.0@Manu343726/testing",
        # "optional-lite/3.1.1@Manu343726/testing",
        # "boost_filesystem/1.66.0@bincrafters/stable",
        # "boost_variant/1.66.0@bincrafters/stable",
        # "boost_optional/1.66.0@bincrafters/stable",
        # "boost_algorithm/1.66.0@bincrafters/stable"
    )

    def source(self):
        self.output.info("cloning sources from {}, checkout {} ...".format(self.options.git_upstream_url, self.version))
        git = tools.Git(folder=self.name)
        git.clone(str(self.options.git_upstream_url), self.version)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.name, defs = {
            "JINJA2CPP_BUILD_TESTS": False,
            "BUILD_SHARED_LIBS": self.options.shared
        })
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src=os.path.join(self.name, "include"))
        self.copy("*.hpp", dst="include", src=os.path.join(self.name, "include"))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["jinja2cpp"]

