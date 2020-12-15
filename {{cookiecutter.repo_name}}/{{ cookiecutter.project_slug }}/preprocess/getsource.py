def getsourceurl():
    '''
    Used by orchestrator to get started with source directory of .csv files.
    Modify DownloadData in orchestrator if files in the directory are not on S3, GCP, Azure or local, e.g. if https
    or if filetype is not .csv
    :return: URI path of directory, not filename, e.g. 's3://myfiles/', not 's3://myfiles/a.csv'
    '''
    return '<Add yours here>'
    # return './input_data/'