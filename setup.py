from setuptools import setup, find_packages

setup(name='terminal_model',
      version='0.1',
      description='Simulation/Optimization of hydrogen terminals',
      author='Ella Tintemann',
      author_email='e.tintemann@fz-juelich.de',
      license='MIT',
      packages=find_packages(where='terminal_model'),
      package_dir={'': 'terminal_model'},
      include_package_data=True,
      zip_safe=False)