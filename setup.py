from setuptools import setup, find_packages

setup(name="escape_eschaton",
      version="0.1",
      description="Calculates most optimal path for escaping Eschaton Asteroid Field",
      author='Vineet Joshi',
      author_email='vineetjoshi006@gmail.com',
      scripts=['escape_eschaton.py'],
      packages=find_packages(exclude=["*tests.*"]),
      include_package_data=True,
      # package_dir = {'lib': 'lib'},
      test_suite="tests"
      # data_files=[('docs', docs),('binner' , bld)]
    )