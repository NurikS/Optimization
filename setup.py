from distutils.core import setup


with open('VERSION', 'r') as fin:
    version = fin.readline().strip()

with open('requirements.txt', 'r') as fin:
    requirements = fin.readlines()

setup(
    name='sugar_optimizer',
    description='Optimizer of sugar consumption',
    version=version,
    python_requires=">=3.6",
    packages=[
        'sugar_optimizer'
        ],
    install_requires=requirements
)
