%define module semver
%bcond_without tests

Name:		python-semver
Version:	3.0.4
Release:	2
Summary:	Python helper for Semantic Versioning (https://semver.org)
URL:		https://github.com/python-semver/python-semver
License:	BSD-3-Clause
Group:		Development/Python
Source0:	https://github.com/python-semver/python-semver/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildSystem:	python

BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
%endif

%description
Python helper to simplify Semantic Versioning (https://semver.org)

%prep
%autosetup -n %{name}-%{version} -p1

# Remove bundled egg-info
rm -rf src/%{module}.egg-info

# Remove git badge remote images from README
sed -i '77,107d;' README.rst

# Remove cov from pytests, dont need those for RPM build.
sed -i 's/--[^ ]*cov[^ ]*//g' .pytest.ini

%build
export SETUPTOOLS_SCM_PRETEND_VERSION="%{version}"
%py_build

%install
%py_install

%if %{with tests}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitearch}:${PWD}"
pytest
%endif

%files
%{_bindir}/py%{module}
%{py_sitedir}/semver
%{py_sitedir}/semver-*.*-info
%doc CHANGELOG.rst
%doc README.rst
%doc SUPPORT.md
%license LICENSE.txt
