import boto3
#23aug18jut: the next line imports botocore.client Config and has to be flagged out when code runs in session mode from local
from botocore.client import Config
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):



    #23aug18jut: this is the session handling used when python is called from local (cli)
    #23aug18jut: s3 allocation by boto3 needs to be done by additional Config parms, see also import section of this code
    #session = boto3.session.Session(profile_name='globi')
    #s3 = session.resource('s3')

    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:491875279524:jut-myPortfolioDeploymentTopic')

    try:

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

        topic.publish(Subject='jutEduc: update was successful', Message='jutEduc: update was successful')

    except:
        topic.publish(Subject='jutEduc: update not successful', Message='jutEduc: update not successful')
        raise


    # TODO implement
    return 'Greetings from Lambda'
