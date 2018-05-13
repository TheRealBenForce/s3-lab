from troposphere import GetAtt, Join, Output
from troposphere import Parameter, Ref, Template
from troposphere.cloudfront import Distribution, DistributionConfig
from troposphere.cloudfront import Origin, DefaultCacheBehavior
from troposphere.cloudfront import ForwardedValues
from troposphere.cloudfront import S3Origin


t = Template()

t.add_description(
    "Deploys a serverless static website with lots "
    "of features and a pipeline.")

paramSiteBucketName = t.add_parameter(Parameter(
    "SiteBucketName",
    Description="The DNS name of an existing S3 bucket to use as the "
                "Cloudfront distribution origin",
    Type="String",
))

resourceMyDistribution = t.add_resource(Distribution(
    "myDistribution",
    DistributionConfig=DistributionConfig(
        Origins=[Origin(Id="Origin 1", DomainName=Ref(paramSiteBucketName),
                        S3OriginConfig=S3Origin())],
        DefaultCacheBehavior=DefaultCacheBehavior(
            TargetOriginId="Origin 1",
            ForwardedValues=ForwardedValues(
                QueryString=False
            ),
            ViewerProtocolPolicy="allow-all"),
        Enabled=True,
        HttpVersion='http2'
    )
))

t.add_output([
    Output("DistributionId", Value=Ref(resourceMyDistribution)),
    Output(
        "DistributionName",
        Value=Join("", ["http://", GetAtt(
            resourceMyDistribution, "DomainName")])),
])

print(t.to_yaml())
