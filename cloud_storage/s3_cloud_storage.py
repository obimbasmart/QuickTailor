#!/usr/bin/env python3

"""
This module encapsulates functionality for
interacting with AWS S3 (Simple Storage Service).
"""

from typing import List, Dict
from uuid import uuid4
import boto3
from os import getenv
from werkzeug.datastructures.file_storage import FileStorage


class S3StorageService():
    __allowed_file_types = ['png', 'jpeg', 'pdf', 'svg', 'jpg']
    __presigned_url_exp_time = 3600

    def __init__(self, bucket_name: str) -> None:
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY'),
            region_name='eu-north-1'
        )

    def __is_valid_file_extenstion(self, filename):
        file_ext = filename.split('.')[-1]
        print(file_ext)
        return file_ext in S3StorageService.__allowed_file_types

    def upload_file(self, file: FileStorage, tailor_id: str,
                    product_id: str) -> str:
        """
        :param file: file object from flask form
        :param tailor_id: tailor's id
        :param product_id: product id
        :raises: TypeError - invalid file type
        :return: img url
        """
        if not self.__is_valid_file_extenstion(file.filename):
            raise TypeError("Invalid file type")

        key_name = f'tailor-{tailor_id}/product-{product_id}/{str(uuid4().hex)}'
        self.s3_client.upload_fileobj(file, self.bucket_name, key_name,
                                      ExtraArgs={'ContentType': file.mimetype})
        return key_name

    def generate_presigned_url(self, action_type: str, key_name: str) -> str:
        """generate aws s3 url for performing actions on an object

        :param action_type: 'get_object' | 'put_object' | 'delete_object'
        :param key_name: object key
        :return: presigned url
        """
        img_url = self.s3_client.generate_presigned_url(
            action_type,
            Params={'Bucket': self.bucket_name, 'Key': key_name},
            ExpiresIn=S3StorageService.__presigned_url_exp_time
        )
        return img_url
    
    def generate_presigned_urls(self, action_type: str, key_names: List[str]) -> List[str]:
        return [
            self.generate_presigned_url('get_object', key)
            for key in key_names
        ]

    def upload_files(self, files: List[FileStorage], tialor_id, product_id) -> Dict[str, str]:
        img_urls = [
            self.upload_file(file, tialor_id, product_id)
            for file in files
        ]
        return {
            f'img_{idx}': img_urls[idx] for idx in range(len(img_urls))
        }

    def delete_file(self, filename):
        return self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)

    def delete_files(self, filenames: List[str]) -> None:
        [
            self.delete_file(filename)
            for filename in filenames
        ]
