"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestBucketFromScheme(object):

    @let
    def fake_bucket_path(self):
        return self.faker.uri_path()

    @let
    def fake_relative_path(self):
        return self.faker.uri_path()[1:]

    @let
    def s3_bucket_path(self):
        return 's3://' + self.fake_bucket_path

    @let
    def gcp_bucket_path(self):
        return 'gs://' + self.fake_bucket_path

    def test_returns_archive_configurations_with_s3_scheme(self):
        from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive

        self._configuration['results_config']['archive_end_point'] = self.s3_bucket_path
        result_config = self.translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual(BucketPipelineArchive, config['archive_type'])
    
    def test_returns_constructor_arguments_with_s3_scheme(self):
        from foundations_aws.aws_bucket import AWSBucket

        self._configuration['results_config']['archive_end_point'] = self.s3_bucket_path
        result_config = self.translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual([AWSBucket, self.fake_bucket_path + '/archive'], config['constructor_arguments'])

    def test_returns_archive_configurations_with_gcp_scheme(self):
        from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive

        self._configuration['results_config']['archive_end_point'] = self.gcp_bucket_path
        result_config = self.translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual(BucketPipelineArchive, config['archive_type'])
    
    def test_returns_constructor_arguments_with_gcp_scheme(self):
        from foundations_gcp.gcp_bucket import GCPBucket

        self._configuration['results_config']['archive_end_point'] = self.gcp_bucket_path
        result_config = self.translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual([GCPBucket, self.fake_bucket_path + '/archive'], config['constructor_arguments'])
    
    def test_returns_archive_configurations_with_default(self):
        from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive

        self._configuration['results_config']['archive_end_point'] = self.fake_bucket_path
        result_config = self.translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual(BucketPipelineArchive, config['archive_type'])
    
    def test_returns_constructor_arguments_with_default(self):
        self._configuration['results_config']['archive_end_point'] = self.fake_bucket_path
        result_config = self.translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual([self.bucket_type, self.fake_bucket_path + '/archive'], config['constructor_arguments'])

    def test_returns_archive_listing_configurations_with_s3_scheme(self):
        from foundations_contrib.bucket_pipeline_listing import BucketPipelineListing

        self._configuration['results_config']['archive_end_point'] = self.s3_bucket_path
        result_config = self.translator.translate(self._configuration)
        config = result_config['archive_listing_implementation']
        self.assertEqual(BucketPipelineListing, config['archive_listing_type'])

    def test_returns_archive_listing_configurations_constructor_arguments_with_s3_scheme(self):
        from foundations_aws.aws_bucket import AWSBucket

        self._configuration['results_config']['archive_end_point'] = self.s3_bucket_path
        result_config = self.translator.translate(self._configuration)
        config = result_config['archive_listing_implementation']
        self.assertEqual([AWSBucket, self.fake_bucket_path + '/archive'], config['constructor_arguments'])

    def test_returns_archive_listing_configurations_with_gcp_scheme(self):
        from foundations_contrib.bucket_pipeline_listing import BucketPipelineListing

        self._configuration['results_config']['archive_end_point'] = self.gcp_bucket_path
        result_config = self.translator.translate(self._configuration)
        config = result_config['archive_listing_implementation']
        self.assertEqual(BucketPipelineListing, config['archive_listing_type'])

    def test_returns_project_listing_configurations_with_s3_scheme(self):
        from foundations_contrib.bucket_pipeline_listing import BucketPipelineListing

        self._configuration['results_config']['archive_end_point'] = self.s3_bucket_path
        result_config = self.translator.translate(self._configuration)
        config = result_config['project_listing_implementation']
        self.assertEqual(BucketPipelineListing, config['project_listing_type'])

    def test_returns_project_listing_configurations_constructor_arguments_with_s3_scheme(self):
        from foundations_aws.aws_bucket import AWSBucket

        self._configuration['results_config']['archive_end_point'] = self.s3_bucket_path
        result_config = self.translator.translate(self._configuration)
        config = result_config['project_listing_implementation']
        self.assertEqual([AWSBucket, self.fake_bucket_path + '/projects'], config['constructor_arguments'])

    def test_returns_project_listing_configurations_with_gcp_scheme(self):
        from foundations_contrib.bucket_pipeline_listing import BucketPipelineListing

        self._configuration['results_config']['archive_end_point'] = self.gcp_bucket_path
        result_config = self.translator.translate(self._configuration)
        config = result_config['project_listing_implementation']
        self.assertEqual(BucketPipelineListing, config['project_listing_type'])

    def test_returns_cache_configurations_with_s3_scheme(self):
        from foundations_contrib.bucket_cache_backend_for_config import BucketCacheBackendForConfig

        self._configuration['cache_config']['end_point'] = self.s3_bucket_path
        result_config = self.translator.translate(self._configuration)
        config = result_config['cache_implementation']
        self.assertEqual(BucketCacheBackendForConfig, config['cache_type'])

    def test_returns_cache_configurations_constructor_arguments_with_s3_scheme(self):
        from foundations_aws.aws_bucket import AWSBucket

        self._configuration['cache_config']['end_point'] = self.s3_bucket_path
        result_config = self.translator.translate(self._configuration)
        config = result_config['cache_implementation']
        self.assertEqual([AWSBucket, self.fake_bucket_path + '/cache'], config['constructor_arguments'])

    def test_returns_cache_configurations_with_gcp_scheme(self):
        from foundations_contrib.bucket_cache_backend_for_config import BucketCacheBackendForConfig

        self._configuration['cache_config']['end_point'] = self.gcp_bucket_path
        result_config = self.translator.translate(self._configuration)
        config = result_config['cache_implementation']
        self.assertEqual(BucketCacheBackendForConfig, config['cache_type'])