﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import random
import json
import hashlib
import hmac
import urllib

class InstagramAPI:
    API_URL = 'https://i.instagram.com/api/v1/'
    USER_AGENT = 'Instagram 8.0.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)'
    IG_SIG_KEY = '9b3b9e55988c954e51477da115c58ae82dcae7ac01c735b4443a3c5923cb593a'
    EXPERIMENTS = 'ig_android_progressive_jpeg,ig_creation_growth_holdout,ig_android_report_and_hide,ig_android_new_browser,ig_android_enable_share_to_whatsapp,ig_android_direct_drawing_in_quick_cam_universe,ig_android_huawei_app_badging,ig_android_universe_video_production,ig_android_asus_app_badging,ig_android_direct_plus_button,ig_android_ads_heatmap_overlay_universe,ig_android_http_stack_experiment_2016,ig_android_infinite_scrolling,ig_fbns_blocked,ig_android_white_out_universe,ig_android_full_people_card_in_user_list,ig_android_post_auto_retry_v7_21,ig_fbns_push,ig_android_feed_pill,ig_android_profile_link_iab,ig_explore_v3_us_holdout,ig_android_histogram_reporter,ig_android_anrwatchdog,ig_android_search_client_matching,ig_android_high_res_upload_2,ig_android_new_browser_pre_kitkat,ig_android_2fac,ig_android_grid_video_icon,ig_android_white_camera_universe,ig_android_disable_chroma_subsampling,ig_android_share_spinner,ig_android_explore_people_feed_icon,ig_explore_v3_android_universe,ig_android_media_favorites,ig_android_nux_holdout,ig_android_search_null_state,ig_android_react_native_notification_setting,ig_android_ads_indicator_change_universe,ig_android_video_loading_behavior,ig_android_black_camera_tab,liger_instagram_android_univ,ig_explore_v3_internal,ig_android_direct_emoji_picker,ig_android_prefetch_explore_delay_time,ig_android_business_insights_qe,ig_android_direct_media_size,ig_android_enable_client_share,ig_android_promoted_posts,ig_android_app_badging_holdout,ig_android_ads_cta_universe,ig_android_mini_inbox_2,ig_android_feed_reshare_button_nux,ig_android_boomerang_feed_attribution,ig_android_fbinvite_qe,ig_fbns_shared,ig_android_direct_full_width_media,ig_android_hscroll_profile_chaining,ig_android_feed_unit_footer,ig_android_media_tighten_space,ig_android_private_follow_request,ig_android_inline_gallery_backoff_hours_universe,ig_android_direct_thread_ui_rewrite,ig_android_rendering_controls,ig_android_ads_full_width_cta_universe,ig_video_max_duration_qe_preuniverse,ig_android_prefetch_explore_expire_time,ig_timestamp_public_test,ig_android_profile,ig_android_dv2_consistent_http_realtime_response,ig_android_enable_share_to_messenger,ig_explore_v3,ig_ranking_following,ig_android_pending_request_search_bar,ig_android_feed_ufi_redesign,ig_android_video_pause_logging_fix,ig_android_default_folder_to_camera,ig_android_video_stitching_7_23,ig_android_profanity_filter,ig_android_business_profile_qe,ig_android_search,ig_android_boomerang_entry,ig_android_inline_gallery_universe,ig_android_ads_overlay_design_universe,ig_android_options_app_invite,ig_android_view_count_decouple_likes_universe,ig_android_periodic_analytics_upload_v2,ig_android_feed_unit_hscroll_auto_advance,ig_peek_profile_photo_universe,ig_android_ads_holdout_universe,ig_android_prefetch_explore,ig_android_direct_bubble_icon,ig_video_use_sve_universe,ig_android_inline_gallery_no_backoff_on_launch_universe,ig_android_image_cache_multi_queue,ig_android_camera_nux,ig_android_immersive_viewer,ig_android_dense_feed_unit_cards,ig_android_sqlite_dev,ig_android_exoplayer,ig_android_add_to_last_post,ig_android_direct_public_threads,ig_android_prefetch_venue_in_composer,ig_android_bigger_share_button,ig_android_dv2_realtime_private_share,ig_android_non_square_first,ig_android_video_interleaved_v2,ig_android_follow_search_bar,ig_android_last_edits,ig_android_video_download_logging,ig_android_ads_loop_count_universe,ig_android_swipeable_filters_blacklist,ig_android_boomerang_layout_white_out_universe,ig_android_ads_carousel_multi_row_universe,ig_android_mentions_invite_v2,ig_android_direct_mention_qe,ig_android_following_follower_social_context'
    SIG_KEY_VERSION = '4'

    #username            # Instagram username
    #password            # Instagram password
    #debug               # Debug
    #uuid                # UUID
    #device_id           # Device ID
    #username_id         # Username ID
    #token               # _csrftoken
    #isLoggedIn          # Session status
    #rank_token          # Rank token
    #IGDataPath          # Data storage path

    def __init__(self, username, password, debug = False, IGDataPath = None):
        m = hashlib.md5()
        m.update(username.encode('utf-8') + password.encode('utf-8'))
        self.device_id = self.generateDeviceId(m.hexdigest())
        self.setUser(username, password)
        self.isLoggedIn = False
        self.LastResponse = None

    def setUser(self, username, password):
        self.username = username
        self.password = password

        self.uuid = self.generateUUID(True)

        # TODO save data to file...

    def login(self, force = False):
        if (not self.isLoggedIn or force):
            self.s = requests.Session()
            # if you need proxy make something like this:
            # self.s.proxies = {"https" : "http://proxyip:proxyport"}
            if (self.SendRequest('si/fetch_headers/?challenge_type=signup&guid=' + self.generateUUID(False), None, True)):

                data = {'phone_id'   : self.generateUUID(True),
                        '_csrftoken' : self.LastResponse.cookies['csrftoken'],
                        'username'   : self.username,
                        'guid'       : self.uuid,
                        'device_id'  : self.device_id,
                        'password'   : self.password,
                        'login_attempt_count' : '0'}

                if (self.SendRequest('accounts/login/', self.generateSignature(json.dumps(data)), True)):
                    print ("Login success!")
                    self.isLoggedIn = True
                    self.username_id = self.LastJson["logged_in_user"]["pk"]
                    print (self.username_id)
                    self.rank_token = "%s_%s" % (self.username_id, self.uuid)
                    self.token = self.LastResponse.cookies["csrftoken"]

                    self.syncFeatures()
                    self.autoCompleteUserList()
                    self.timelineFeed()
                    self.getv2Inbox()
                    self.getRecentActivity()

                    return True;

    def tagFeed(self, tag):
        userFeed = self.SendRequest("feed/tag/"+ tag +"/?rank_token=" + self.rank_token + "&ranked_content=true&")
        # TODO Instagram.php 1000-1015
        return userFeed

    def like(self, mediaId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        '_csrftoken'    : self.token,
        'media_id'      : mediaId
        })

        return self.SendRequest("media/"+ str(mediaId) +"/like/", self.generateSignature(data))

    def SendRequest(self, endpoint, post = None, login = False):
        if (not self.isLoggedIn and not login):
            raise Exception("Not logged in!\n")
            return;

        self.s.headers.update ({'Connection' : 'close',
                                'Accept' : '*/*',
                                'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Cookie2' : '$Version=1',
                                'Accept-Language' : 'en-US',
                                'User-Agent' : self.USER_AGENT})

        if (post != None): # POST
            response = self.s.post(self.API_URL + endpoint, data=post) # , verify=False
        else: # GET
            response = self.s.get(self.API_URL + endpoint) # , verify=False

        if response.status_code == 200:
            self.LastResponse = response
            self.LastJson = json.loads(response.text)
            return True
        else:
            print ("Request return " + str(response.status_code) + " error!")
            return False

    def generateUUID(self, type):
        uuid = '%04x%04x-%04x-%04x-%04x-%04x%04x%04x' % (random.randint(0, 0xffff),
               random.randint(0, 0xffff), random.randint(0, 0xffff),
               random.randint(0, 0x0fff) | 0x4000,
               random.randint(0, 0x3fff) | 0x8000,
               random.randint(0, 0xffff), random.randint(0, 0xffff),
               random.randint(0, 0xffff))
        if (type):
            return uuid
        else:
            return uuid.replace('-', '')

    def generateDeviceId(self, seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    def generateSignature(self, data):
        return 'ig_sig_key_version=' + self.SIG_KEY_VERSION + '&signed_body=' + hmac.new(self.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + urllib.parse.quote(data)

    def syncFeatures(self):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'id'            : self.username_id,
        '_csrftoken'    : self.token,
        'experiments'   : self.EXPERIMENTS
        })
        return self.SendRequest('qe/sync/', self.generateSignature(data))

    def autoCompleteUserList(self):
        return self.SendRequest('friendships/autocomplete_user_list/')

    def timelineFeed(self):
        return self.SendRequest('feed/timeline/')

    def megaphoneLog(self):
        return self.SendRequest('megaphone/log/')

    def expose(self):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        'id'           : self.username_id,
        '_csrftoken'   : self.token,
        'experiment'   : 'ig_android_profile_contextual_feed'
        })
        return self.SendRequest('qe/expose/', self.generateSignature(data))

    def logout(self):
        logout = self.SendRequest('accounts/logout/')
        # TODO Instagram.php 180-185

    def uploadPhoto(self, photo, caption = None, upload_id = None):
        # TODO Instagram.php 200-290
        return False

    def uploadVideo(self, video, caption = None):
        # TODO Instagram.php 290-415
        return False

    def direct_share(self, media_id, recipients, text = None):
        # TODO Instagram.php 420-490
        return False

    def configureVideo(upload_id, video, caption = ''):
        # TODO Instagram.php 490-530
        return False

    def configure(upload_id, photo, caption = ''):
        # TODO Instagram.php 530-570
        return False

    def editMedia(self, mediaId, captionText = ''):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'caption_text' : captionText
        })
        return self.SendRequest("media/"+ str(mediaId) +"/edit_media/", self.generateSignature(data))

    def removeSelftag(self, mediaId):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token
        })
        return self.SendRequest("media/"+ str(mediaId) +"/remove/", self.generateSignature(data))

    def mediaInfo(self, mediaId):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'media_id'     : mediaId
        })
        return self.SendRequest("media/"+ str(mediaId) +"/info/", self.generateSignature(data))

    def deleteMedia(self, mediaId):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'media_id'     : mediaId
        })
        return self.SendRequest("media/"+ str(mediaId) +"/delete/", self.generateSignature(data))

    def comment(self, mediaId, commentText):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'comment_text' : commentText
        })
        return self.SendRequest("media/"+ str(mediaId) +"/comment/", self.generateSignature(data))

    def deleteComment(self, mediaId, captionText, commentId):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'caption_text' : captionText
        })
        return self.SendRequest("media/"+ str(mediaId) +"/comment/"+ str(commentId) +"/delete/", self.generateSignature(data))

    def changeProfilePicture(photo):
        # TODO Instagram.php 705-775
        return False

    def getv2Inbox(self):
        inbox = self.SendRequest('direct_v2/inbox/?')
        # TODO Instagram.php 950-960
        return inbox

    def getRecentActivity(self):
        activity = self.SendRequest('news/inbox/?')
        # TODO Instagram.php 911-925
        return activity

InstagramAPI = InstagramAPI("login", "password")
InstagramAPI.login() # login
InstagramAPI.tagFeed("cat") # get media list by tag #cat
media_id = InstagramAPI.LastJson["ranked_items"][0]["pk"] # media id of first media
InstagramAPI.like(media_id) # like first media
