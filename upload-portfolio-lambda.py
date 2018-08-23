import boto3
import StringIO
import zipfile
import mimetypes



session = boto3.session.Session(profile_name='globi')
s3 = session.resource('s3')



myoriginbucket = s3.Bucket('jut-virginia-serverless')
mytargetbucket = s3.Bucket('jutzi.awstt.xyz')
mymemory = StringIO.StringIO()

myoriginbucket.download_fileobj('portfoliobuild.zip', mymemory)

with zipfile.ZipFile(mymemory) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        mytargetbucket.upload_fileobj(obj, nm,
        ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        mytargetbucket.Object(nm).Acl().put(ACL='public-read')
