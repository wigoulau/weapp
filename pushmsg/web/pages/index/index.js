//index.js
//获取应用实例
const app = getApp()

Page({
  globalData: {
    appid: 'wx680a64db68bd9fee',
    secret: 'e4bcb9d50fa76976dcfc6171e0d85769',
  },
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    var that = this;
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
    wx.login({
      success: function(res) {
        if (res.code) {
          console.log('res.code is ' + res.code);
          var dat = that.globalData;
          console.log('appid')
          var url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + dat.appid + '&secret=' + dat.secret + '&js_code=' + res.code + '&grant_type=authorization_code';
          console.log(url);
          wx.request({
            url: url,
            data: {},
            method: 'GET',
            success: function(res) {
              var obj = {};
              obj.openid = res.data.openid;
              console.log("openid is " + obj.openid);
              console.log("session_key is " + res.data.session_key);
              obj.expires_in = Date.now() + res.data.expires_in;
              wx.setStorageSync('user', obj); // storage openid
            }
          });
        } else {
          console.log('获取用户登录状态失败! ' + res.errMsg)
        }
      }
    })
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },

  getFormID: function (e) {
    console.log('getformid ' + e.detail.formId)
    var obj = {}
    obj = wx.getStorageSync('user')
    wx.request({
      url: 'http://192.168.188.163:4000/department/notification',
      data: {
        'openid': obj.openid,
        'form_id': e.detail.formId
      },
      method: 'POST',
      success: function (response) {
        if (response.statusCode == 200) {
          console.log("data is " + response.data)
        }
      },
      fail: function (error) {
        console.log('error')
        console.log(error)
      }
    })
  },
})
