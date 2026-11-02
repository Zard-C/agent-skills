from conan import ConanFile
from conan.tools.cmake import cmake_layout


class BenchmarkRecipe(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires("benchmark/1.10.0")

    def layout(self):
        cmake_layout(self)
