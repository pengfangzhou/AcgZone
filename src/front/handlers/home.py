# -*- coding: utf-8 -*-

import time
import zlib
import uuid
import random
import pickle
import datetime
from twisted.internet import defer
from cyclone import escape, web
from front import storage
from front import utils
from front.utils import E
from front import D
# from front.handlers.base import BaseHandler
from front.wiapi import *
from front.handlers.base import ApiHandler, ApiJSONEncoder
# os.environ['DJANGO_SETTINGS_MODULE'] = 'back.settings'
from filebrowser.base import FileObject
from twisted.python import log
import logging

class HomeHandler(ApiHandler):

    def get(self):
        self.render('index.html')


class CrossdomainHandler(ApiHandler):

    def get(self):
        self.render('crossdomain.xml')

@handler
class IndexHandler(ApiHandler):

    @storage.databaseSafe
    @defer.inlineCallbacks
    @api('Index', '/', [
        Param('channel', True, str, 'putaogame', 'putaogame', 'channel'),
        Param('access_token', False, str, '55526fcb39ad4e0323d32837021655300f957edc', '55526fcb39ad4e0323d32837021655300f957edc', 'access_token'),
    ], filters=[ps_filter], description="Index")
    def post(self):
        if self.has_arg('channel'):
            channels = yield self.sql.runQuery("SELECT id FROM core_channel WHERE slug=%s LIMIT 1", (self.arg("channel"), ))
            if channels:
                channel, = channels[0]
            else:
                # raise web.HTTPError(404,'channel not find in DB.')
                emsg = "该渠道在记录中不存在"
                logging.error(emsg)
                self.write(dict(err=E.ERR_PARAM, msg=emsg))
                return
        else:
            emsg = "参数中不包括渠道"
            logging.error(emsg)
            self.write(dict(err=E.ERR_PARAM, msg=emsg))
            return
            # raise web.HTTPError('400', 'Argument error. not find channel!')

        if channel:
            #通过core_zone_channels里的channel_id拿到zoneid列表，得到zoneid列表每一个zoneid对应的信息
            res = yield self.sql.runQuery("SELECT a.id, a.zoneid, a.domain, a.maxnum, a.status, a.index FROM core_zone AS a")
            zone_dict = {}
            record = {}
            # print "home.py res: ",res
            if res:
                for r in res:
                    zid, zoneid, domain, maxnum, status, index = r
                    notice_dict = {}
                    # notices = yield self.sql.runQuery("SELECT notice_id, position FROM core_noticeship WHERE zone_id=%s", (zid, ))
                    # if notices:
                    #     for n in notices:
                    #         notices = yield self.sql.runQuery("SELECT id, title, content, screenshot, sign,\
                    #           created_at FROM core_notice WHERE id=%s", (n[0], ))
                    #         nid, title, content, screenshot, sign, create_at = notices[0]
                    #         if screenshot and FileObject(screenshot).exists():
                    #             url = FileObject(screenshot).url
                    #         else:
                    #             url = ''
                    #         create_at = time.mktime(create_at.timetuple())
                    #         position = n[1]
                    #         notice_dict[nid] = dict(title=title, content=content, url=url, sign=sign, create_at=create_at,\
                    #                                 position=position)

                    try:
                        nownum = yield self.redis.get('zone:%s:%s' % (zoneid, datetime.datetime.now().strftime('%Y%m%d')))
                    except Exception:
                        nownum = 0

                    zone_dict[zoneid] = dict(domain=domain, maxnum=maxnum, nownum=nownum, status=status, index=index,\
                                             notices=notice_dict, title=D.ZONENAME.get(str(zoneid), ''))

                    if self.has_arg('access_token'):
                        idcard = yield self.redis.get('zone:%s:%s' % (zoneid, self.arg('access_token')))

                        if idcard:
                            record[zoneid] = idcard
                # if rec:
                #     rec = pickle.loads(rec)
                #     record = rec            

            ret = dict(zone=zone_dict, record=record, timestamp=int(time.time()))
            reb = zlib.compress(escape.json_encode(ret))
            self.write(ret)
        else:
            # raise web.HTTPError(404,'channel not find in DB.')
            emsg = "渠道在记录中不存在"
            logging.error(emsg)
            self.write(dict(err=E.ERR_PARAM, msg=emsg))
            return

@handler
class UpdateHandler(ApiHandler):

    @storage.databaseSafe
    @defer.inlineCallbacks
    @api('Update', '/update/', [
        Param('channel', True, str, 'putaogame', 'putaogame', 'channel'),
        Param('version', True, str, 'v1.1', 'v1.1', 'version'),
    ], filters=[ps_filter], description="Update")
    def get(self):
        try:
            channel = self.get_argument('channel', 'putaogame')
            version = str(self.get_argument('version'))
        except Exception:
            # raise web.HTTPError(400, 'Argument error')
            emsg = "传入参数有误"
            logging.error(emsg)
            self.write(dict(err=E.ERR_PARAM, msg=emsg))
            return

        channels = yield self.sql.runQuery("SELECT id, version, version2, version3 FROM core_channel WHERE slug=%s LIMIT 1", (channel, ))
        if channels:
            channel, nversion, mversion, uversion = channels[0]
        else:
            # raise web.HTTPError(404,'Channel not find in DB core_channel.')
            emsg = "渠道在记录中不存在"
            logging.error(emsg)
            self.write(dict(err=E.ERR_PARAM, msg=emsg))
            return
        #最大版本号需要根据请求版本号和配置版本号来确认
        #请求版本号需要和最大版本号一致
        #确定最大版本号应该使用哪一列
        if version.split('.')[0] == nversion.split('.')[0]:
            max_version = nversion
        elif version.split('.')[0] == mversion.split('.')[0]:
            max_version = mversion
        else:
            max_version = uversion
        # try:
        #     assert version.split('.')[0] == nversion.split('.')[0]
        #     max_version = nversion
        # except Exception:
        #     max_version = mversion
        if cmp(version, max_version) == 0:
            ret = dict(code=0, timestamp=int(time.time())) 
            reb = zlib.compress(escape.json_encode(ret)) 
            self.write(ret)
            return
        FIND = False  
        res = yield self.sql.runQuery("SELECT cversion, tversion, url, sign FROM core_update WHERE channel_id=%s", (channel, ))
        if res: 
            for r in res:
                if version == str(r[0]) and max_version == str(r[1]):
                    FIND = True
                    code, target, url, md5 = 1, r[1], r[2], r[3]
                    ret = dict(code=code, msg='', targetVersion=target, upgrade=url, md5=md5, timestamp=int(time.time()))
                    reb = zlib.compress(escape.json_encode(ret))
                    self.write(ret)
                    return  
                else:continue
        if not FIND:
            res = yield self.sql.runQuery("SELECT version, url, md5 FROM core_upgrade WHERE channel_id=%s ORDER BY version DESC LIMIT 1", (channel, ))
            if res: 
                for r in res:
                    code, target, url, md5 = -1, r[0], r[1] or '', r[2] or ''
                    ret = dict(code=code, msg='', targetVersion=target, upgrade=url, md5=md5, timestamp=int(time.time()))  
                    reb = zlib.compress(escape.json_encode(ret))
                    self.write(ret)
                    return
            else:
                ret = dict(code=0, timestamp=int(time.time())) 
                reb = zlib.compress(escape.json_encode(ret)) 
                self.write(ret)
                return

@handler
class BindHandler(ApiHandler):

    @storage.databaseSafe
    @defer.inlineCallbacks
    @api('Bind Token', '/bind/token/', [
        Param('channel', True, str, 'putaogame', 'putaogame', 'channel'),
        Param('thirdparty_token', True, str, '55526fcb3', '55526fcb3', 'thirdparty_token'),
        Param('access_token', True, str, '55526fcb39ad4e0323d32837021655300f957edc', '55526fcb39ad4e0323d32837021655300f957edc', 'access_token'),
    ], filters=[ps_filter], description="Bind Token")
    def post(self):
        try:
            channel = str(self.get_argument('realChannel'))
            thirdparty_token = str(self.get_argument('thirdparty_token'))
            access_token = str(self.get_argument('access_token'))
        except Exception:
            raise web.HTTPError(400, 'Argument error')
        channels = yield self.sql.runQuery("SELECT id FROM core_channel WHERE slug=%s LIMIT 1", (channel, ))
        if channels:
            channel, = channels[0]
        else:
            raise web.HTTPError(404)
        try:
            res = yield self.sql.runQuery("SELECT * FROM core_bindtoken WHERE channel_id=%s AND thirdparty_token=%s AND access_token=%s",\
             (channel, thirdparty_token, access_token))
            if not res:
                query = "INSERT INTO core_bindtoken(channel_id, thirdparty_token, access_token, timestamp) VALUES (%s, %s, %s, %s) RETURNING id"
                params = (channel, thirdparty_token, access_token, int(time.time()))
                for i in range(5):
                    try:
                        yield self.sql.runQuery(query, params)
                        break
                    except storage.IntegrityError:
                        log.msg("SQL integrity error, retry(%i): %s" % (i, (query % params)))
                        continue
                yield self.redis.hset("bindtoken:%s" % channel, thirdparty_token, access_token)
        except Exception, e:
            print e
        
        ret = dict(timestamp=int(time.time())) 
        reb = zlib.compress(escape.json_encode(ret)) 
        self.write(ret)

@handler
class GetHandler(ApiHandler):

    @storage.databaseSafe
    @defer.inlineCallbacks
    @api('Get Token', '/get/token/', [
        Param('channel', True, str, 'putaogame', 'putaogame', 'channel'),
        Param('realChannel', True, str, 'putaogame', 'putaogame', 'realChannel'),
        Param('thirdparty_token', True, str, '55526fcb3', '55526fcb3', 'thirdparty_token'),
    ], filters=[ps_filter], description="Get Token")
    def post(self):
        try:
            channel = str(self.get_argument('realChannel'))
            thirdparty_token = str(self.get_argument('thirdparty_token'))
        except Exception:
            raise web.HTTPError(400, 'Argument error')
        channels = yield self.sql.runQuery("SELECT id FROM core_channel WHERE slug=%s LIMIT 1", (channel, ))
        if channels:
            channel, = channels[0]
        else:
            raise web.HTTPError(400, 'Argument error')
        try:
            res = yield self.sql.runQuery("SELECT access_token FROM core_bindtoken WHERE channel_id=%s AND thirdparty_token=%s LIMIT 1",\
             (channel, thirdparty_token))
            if res:
                access_token, = res[0]
            else:
                access_token = yield self.redis.hget("bindtoken:%s" % channel, thirdparty_token)
                if not access_token:
                    access_token = ""
        except Exception:
            access_token = ""
        # access_token = yield self.redis.hget("bindtoken:%s" % channel, thirdparty_token)
        # if not access_token:
        #     access_token = ''
        ret = dict(access_token=access_token, timestamp=int(time.time())) 
        reb = zlib.compress(escape.json_encode(ret)) 
        self.write(ret)

@handler
class IdcardHandler(ApiHandler):

    @storage.databaseSafe
    @defer.inlineCallbacks
    @api('Set idcard', '/set/idcard/', [
        Param('zoneid', True, str, '200', '200', 'zoneid'),
        Param('access_token', True, str, '05ba985f2cac3ec082353ebc1712a7c7fe5fe15d', '05ba985f2cac3ec082353ebc1712a7c7fe5fe15d', 'access_token'),
        Param('idcard', True, str, '69bc4774d14a4c28b14f255723cb8f99h1174', '69bc4774d14a4c28b14f255723cb8f99h1174', 'idcard'),
    ], filters=[ps_filter], description="Set idcard")
    def post(self):
        try:
            zoneid = str(self.get_argument('zoneid'))
            access_token = str(self.get_argument('access_token'))
            idcard = str(self.get_argument('idcard'))
        except Exception:
            raise web.HTTPError(400, 'Argument error')
        yield self.redis.set('zone:%s:%s' % (zoneid, access_token), idcard)
        self.write('ok')

@handler
class FlushdbHandler(ApiHandler):

    @storage.databaseSafe
    # @defer.inlineCallbacks
    @api('Flushdb', '/flushdb/', [
    ], filters=[ps_filter], description="Flushdb")
    def post(self):
        self.write("START...\r\n")
        self.redis.flushdb()
        self.write("FLUSHDB SUCCESS")

@handler
class RegisterMemberHandler(ApiHandler):

    @storage.databaseSafe
    @defer.inlineCallbacks
    @api('Member Register', '/user/register/', [
        Param('username', True, str, 'zhanghao', 'zhanghao', 'nickname'),
        Param('password', True, str, '123', '123', 'password'),
        Param('channel', False, str, 'putaogame', 'putaogame', 'channel'),
        Param('realChannel', False, str, 'putaogame', 'putaogame', 'realChannel'),
        Param('client_id', False, str, 'id', 'id', 'client_id'),
        Param('client_secret', False, str, 'secret', 'secret', 'client_secret'),
        Param('source', False, str, 'tv', 'tv', 'source'),
        Param('t', False, str, '123456', '123456', 't'),
        Param('udid', False, str, 'udid', 'udid', 'udid'),
        ], filters=[ps_filter], description="Member Register")
    def post(self):
        # username = "myu"
        # username = yield username
        # self.write("ok")
        try:
            #必须参数
            username = self.get_argument("username")
            password = self.get_argument("password")
            # print "username:",username
            # print "password:",password
        except Exception:
            # raise web.HTTPError(400, "Argument error")
            emsg = "传入参数有误"
            logging.error(emsg)
            self.write(dict(err=E.ERR_PARAM, msg=emsg))
            return

        try:
            #非必须参数
            channel = self.get_argument("channel")
            realChannel = self.get_argument("realChannel")
            client_id = self.get_argument("client_id")
            client_secret = self.get_argument("client_secret")
            source = self.get_argument("source")
            t = self.get_argument("t")
            udid = self.get_argument("udid")
        except Exception:
            print "no extra params info when register"
            channel = '0'
            realChannel = '0'
            client_id = '0'
            client_secret = '0'
            source = '0'
            t = '0'
            udid = '0'
        if username==None or username=='':
            web.HTTPError(401, 'username is empty')

        res = yield self.sql.runQuery("SELECT memberid, username, password FROM core_member WHERE username=%s LIMIT 1", (username, ))
        if not res:
            authstring = uuid.uuid4().hex
            # print "authstring:",authstring
            fronttime = t
            phone = '0'
            model = '0'
            serial = '1'
            created = int(time.time())
            updated = created
            ip = self.request.remote_ip
            #msg len<= 200
            # print len(msg)
            msg ='r'
            query = "INSERT INTO core_member(username,password,clientid,clientsecret,channel,realchannel,authstring,udid,source,phone,model,serial,ip,msg,fronttime,created,updated,question,answer) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING authstring;"
            params = (username,password,client_id,client_secret,channel,realChannel,authstring,udid,source,phone,model,serial,ip,msg,fronttime,created,updated,'','')
            # print "query:",query
            # print "params:",params
            for i in range(5):
                try:
                    sql = yield self.sql.runQuery(query,params)
                    # print "execute ok"
                    break
                except storage.IntegrityError:
                    log.msg("SQL integrity error, retry(%i): %s" % (i, (query % params)))
                    sql = None
                    continue
            if sql:
                authstring = sql[0][0]
                self.write(dict(access_token=authstring))
            else:
                # raise web.HTTPError(500, 'Create member failed')
                emsg = "创建账号失败,请重试。"
                logging.error(emsg)
                self.write(dict(err=E.ERR_DB, msg=emsg))
                return
        else:
            # raise web.HTTPError(400, 'user exist, please try another username')
            emsg = "该账号已经存在，请使用另一个账号注册。"
            logging.error(emsg)
            self.write(dict(err=E.ERR_PARAM, msg=emsg))
            return

@handler
class LoginMemberHandler(ApiHandler):
    @storage.databaseSafe
    @defer.inlineCallbacks
    @api('Member Login', '/user/login/', [
        Param('username', True, str, 'zhanghao', 'zhanghao', 'nickname'),
        Param('password', True, str, '123', '123', 'password'),
        Param('channel', False, str, 'putaogame', 'putaogame', 'channel'),
        Param('realChannel', False, str, 'putaogame', 'putaogame', 'realChannel'),
        Param('client_id', False, str, 'id', 'id', 'client_id'),
        Param('client_secret', False, str, 'secret', 'secret', 'client_secret'),
        Param('source', False, str, 'tv', 'tv', 'source'),
        Param('t', False, str, '123456', '123456', 't'),
        Param('udid', False, str, 'udid', 'udid', 'udid'),
        ], filters=[ps_filter], description="Member Login")
    def post(self):
        try:
            username = self.get_argument("username")
            password = self.get_argument("password")
        except Exception:
            # raise web.HTTPError(400, "Argument error")
            emsg = "传入的参数有误"
            logging.error(emsg)
            self.write(dict(err=E.ERR_PARAM, msg=emsg))
            return
        res = yield self.sql.runQuery("SELECT username,password,authstring FROM core_member WHERE username=%s LIMIT 1", (username, ))
        if not res:
            # raise web.HTTPError(401, "User does not exist")
            emsg = "账号不存在，请点击注册按钮注册该账号。"
            logging.error(emsg)
            self.write(dict(err=E.ERR_DB, msg=emsg))
            return
        else:
            duname,dpwd,dauthstring = res[0]
            if password == dpwd:
                # print "dauthstring:",dauthstring
                self.write(dict(access_token=dauthstring))
            else:
                # raise web.HTTPError(401, "Password error, Try Again.")
                emsg = "密码输入错误，请重试。"
                logging.error(emsg)
                self.write(dict(err=E.ERR_DB, msg=emsg))
                return

@handler
class QuickRegisterMemberHandler(ApiHandler):
    @storage.databaseSafe
    @defer.inlineCallbacks
    @api('Member Quick Register', '/user/create/', [
        Param('channel', False, str, 'putaogame', 'putaogame', 'channel'),
        Param('realChannel', False, str, 'putaogame', 'putaogame', 'realChannel'),
        Param('client_id', False, str, 'id', 'id', 'client_id'),
        Param('client_secret', False, str, 'secret', 'secret', 'client_secret'),
        Param('source', False, str, 'tv', 'tv', 'source'),
        Param('t', False, str, '123456', '123456', 't'),
        Param('udid', False, str, 'udid', 'udid', 'udid'),
        ], filters=[ps_filter], description="Member Register")
    def post(self):
        try:
            #非必须参数
            channel = self.get_argument("channel")
            realChannel = self.get_argument("realChannel")
            client_id = self.get_argument("client_id")
            client_secret = self.get_argument("client_secret")
            source = self.get_argument("source")
            t = self.get_argument("t")
            udid = self.get_argument("udid")
        except Exception:
            print "no extra params info when register"
            channel = '0'
            realChannel = '0'
            client_id = '0'
            client_secret = '0'
            source = '0'
            t = '0'
            udid = '0'

        authstring = uuid.uuid4().hex
        username = authstring
        password = ""
        # print "authstring:",authstring
        fronttime = t
        phone = '0'
        model = '0'
        serial = '0'
        created = int(time.time())
        updated = created
        ip = self.request.remote_ip
        #msg len<= 200
        # print len(msg)
        msg ='q'

        query = "INSERT INTO core_member(username,password,clientid,clientsecret,channel,realchannel,authstring,udid,source,phone,model,serial,ip,msg,fronttime,created,updated,question,answer) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING authstring;"
        params = (username,password,client_id,client_secret,channel,realChannel,authstring,udid,source,phone,model,serial,ip,msg,fronttime,created,updated,'','')
         # print "query:",query
        # print "params:",params
        for i in range(5):
            try:
                sql = yield self.sql.runQuery(query,params)
                # print "execute ok"
                break
            except storage.IntegrityError:
                log.msg("SQL integrity error, retry(%i): %s" % (i, (query % params)))
                sql = None
                continue

        if sql:
            rauthstring = authstring
            self.write(dict(access_token=rauthstring))
        else:
            # raise web.HTTPError(500, 'Create member failed')
            emsg = "快速游戏创建信息失败，请重试或注册账号并登陆。"
            logging.error(emsg)
            self.write(dict(err=E.ERR_DB, msg=emsg))
            return

@handler
class BindMemberHandler(ApiHandler):
    @storage.databaseSafe
    @defer.inlineCallbacks
    @api('Member Login', '/user/bind/', [
        Param('username', True, str, 'zhanghao', 'zhanghao', 'nickname'),
        Param('password', True, str, '123', '123', 'password'),
        Param('access_token', True, str, '123', '123', 'password'),
        Param('channel', False, str, 'putaogame', 'putaogame', 'channel'),
        Param('realChannel', False, str, 'putaogame', 'putaogame', 'realChannel'),
        Param('client_id', False, str, 'id', 'id', 'client_id'),
        Param('client_secret', False, str, 'secret', 'secret', 'client_secret'),
        Param('source', False, str, 'tv', 'tv', 'source'),
        Param('t', False, str, '123456', '123456', 't'),
        Param('udid', False, str, 'udid', 'udid', 'udid'),
        ], filters=[ps_filter], description="Member Login")
    def post(self):
        try:
            username = self.get_argument("username")
            password = self.get_argument("password")
            authstring = self.get_argument("access_token")
        except Exception:
            # raise web.HTTPError(400, "Argument error")
            emsg = "传入参数有误。"
            logging.error(emsg)
            self.write(dict(err=E.ERR_PARAM, msg=emsg))
            return

        if username==None or username=='':
            # web.HTTPError(401, 'username is empty')
            emsg = "输入的账号是空的"
            logging.error(emsg)
            self.write(dict(err=E.ERR_PARAM, msg=emsg))
            return

        resUsername = yield self.sql.runQuery("SELECT username FROM core_member WHERE username=%s and serial = '1' LIMIT 1", (username, ))
        if resUsername:
            # raise web.HTTPError(401, "username is exist")
            emsg = "该账号已经存在，请更换一个。"
            logging.error(emsg)
            self.write(dict(err=E.ERR_DB, msg=emsg))
            return

        resToken = yield self.sql.runQuery("SELECT username,password,authstring,msg FROM core_member WHERE authstring=%s LIMIT 1", (authstring, ))
        if resToken:
            (dusername,dpassword,dauthstring,dmsg) = resToken[0];
            #check msg
            if len(dmsg)>200: dmsg='s'+len(dmsg.split(','))
            updated = int(time.time())
            dmsg = dmsg+"_b"+str(updated)
            serial = "1"
            #update: username,password,msg,updated
            updateQuery = "update core_member set username=%s,password=%s,msg=%s,updated=%s,serial=%s where authstring=%s RETURNING authstring";
            updateParams = (username,password,dmsg,updated,serial,authstring);
            try:
                sql = yield self.sql.runQuery(updateQuery,updateParams)
            except storage.IntegrityError:
                log.msg("SQL integrity error: %s" % (updateQuery % updateParams))
                sql = None
            if sql:
                self.write(dict(resultmsg="success"))
            else:
                self.write(dict(resultmsg="fail"))
        else:
            # raise web.HTTPError(401, "access_token is not exist")
            emsg = "token 不存在"
            logging.error(emsg)
            self.write(dict(err=E.ERR_DB, msg=emsg))
            return

