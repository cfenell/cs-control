from distutils.core import setup

setup(name = "RefaceControl", 
      version="20180610", 
      author="Carl-Fredrik Enell",
      author_email="fredrik@kyla.kiruna.se",
      url="http://kyla.kiruna.se/~fredrik/",
      package_dir={'':'modules'},
      packages = [''],
      scripts = ['scripts/cs_setsound','scripts/cs_getsound']
)

