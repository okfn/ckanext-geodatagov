
import logging
from nose.tools import assert_equal, assert_in
from ckan import plugins as p
try:
    from ckan.tests.helpers import reset_db
    from ckan.tests import factories
except ImportError:
    from ckan.new_tests.helpers import reset_db
    from ckan.new_tests import factories
from nose.plugins.skip import SkipTest

log = logging.getLogger(__name__)


class TestFixPkg(object):

    @classmethod
    def setup_class(cls):
        if p.toolkit.check_ckan_version(max_version='2.3'):
            raise SkipTest('Just for CKAN 2.8, we just change tags behaviour for 2.8')

    @classmethod
    def setup(cls):
        reset_db()
        cls.organization = factories.Organization() 

    def test_fix_tags(self):
        dataset_extras = [
            {
                "key": "tags",
                "value": "tag01, tag02"
            }
        ]
        dataset = factories.Dataset(
            owner_org=self.organization['id'],
            extras=dataset_extras)
        
        assert_in("tag01", [t['name'] for t in dataset['tags']])
        assert_in("tag02", [t['name'] for t in dataset['tags']])
    
    def test_avoid_duplicated_tags(self):
        dataset_extras = [
            {
                "key": "tags",
                "value": "tag01, tag02"
            }
        ]
        dataset = factories.Dataset(
            owner_org=self.organization['id'],
            extras=dataset_extras,
            tags=[{'name': 'tag01'}])
        
        assert_equal(len(dataset['tags']), 2)
        assert_in("tag01", [t['name'] for t in dataset['tags']])
        assert_in("tag02", [t['name'] for t in dataset['tags']])
