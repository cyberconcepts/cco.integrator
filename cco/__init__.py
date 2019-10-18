# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
from typing import Iterable
__path__ : Iterable[str]
try:
    __import__('pkg_resources').declare_namespace(__name__) # type: ignore
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)
