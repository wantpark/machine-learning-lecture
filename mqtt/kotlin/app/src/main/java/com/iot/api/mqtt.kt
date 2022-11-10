package com.iot.api

import android.annotation.SuppressLint
import android.content.Context
import android.util.Log
import java.security.SecureRandom
import java.security.cert.X509Certificate
import javax.net.ssl.HostnameVerifier
import javax.net.ssl.SSLContext
import javax.net.ssl.TrustManager
import javax.net.ssl.X509TrustManager
import java.util.UUID
import org.eclipse.paho.android.service.MqttAndroidClient
import org.eclipse.paho.client.mqttv3.*
import org.json.JSONException
import org.json.JSONObject

class MQTT: MqttCallback {
    private val config = Config()

    private var cse: String? = null
    private var ae: String? = null
    private var container: String? = null
    private var subscribe: String? = null

    private lateinit var client: MqttAndroidClient
    private lateinit var recv: (String) -> Unit

    override fun connectionLost(cause: Throwable?) {
    }

    override fun deliveryComplete(token: IMqttDeliveryToken?) {
    }

    override fun messageArrived(topic: String?, message: MqttMessage) {
        try {
            val json = JSONObject(message.toString())
            val con = json.getJSONObject("pc").getJSONObject("m2m:sgn").getJSONObject("nev")
                .getJSONObject("rep")
                .getJSONObject("m2m:cin").getString("con")

            // 사용자가 입력한 데이터/이벤트를 전달한다.
            this.recv(con.toString())

            // 정상적으로 받았다는 것을 모비우스에 알린다.
            client.publish("/oneM2M/resp/${this.cse}/${this.ae}/${this.container}/${this.subscribe}/json",
                MqttMessage(JSONObject().put("rsc", "2000").put("rqi", json.getString("rqi")).put("pc", "").toString().toByteArray()))
        } catch (e: JSONException) {
            e.printStackTrace()
        }
    }

    private fun acceptUnauthorized(): SSLContext {
        val trustAllCerts = arrayOf<TrustManager>(object : X509TrustManager {
            override fun getAcceptedIssuers(): Array<X509Certificate> {
                return arrayOf()
            }

            @SuppressLint("TrustAllX509TrustManager")
            override fun checkClientTrusted(certs: Array<X509Certificate>, authType: String) {
            }

            @SuppressLint("TrustAllX509TrustManager")
            override fun checkServerTrusted(certs: Array<X509Certificate>, authType: String) {
            }
        })

        val context = SSLContext.getInstance("SSL")
        context.init(null, trustAllCerts, SecureRandom())

        return context
    }

    fun connect(
        context: Context,
        recv: (String) -> Unit,
        ae: String,
        container: String,
        subscribe: String,
        cse: String = "Mobius2"
    ) {
        this.cse = cse
        this.ae = ae
        this.container = container
        this.subscribe = subscribe
        this.recv = recv

        val protocol = if (config.USE_SECURE) "ssl://" else "tcp://"
        val address = if (config.USE_SECURE) config.MQTT_URL else config.MQTT_IP

        try {
            client = MqttAndroidClient(context, "$protocol$address:${config.MQTT_PORT}", UUID.randomUUID().toString().replace("-","").substring(0,8))

            val options = MqttConnectOptions()
            options.connectionTimeout = 60
            options.keepAliveInterval = 60
            options.mqttVersion = MqttConnectOptions.MQTT_VERSION_3_1

            if (config.USE_SECURE) {
                options.socketFactory = acceptUnauthorized().socketFactory
                options.sslHostnameVerifier = HostnameVerifier { _, _ -> true }
            }

            Log.d("API", "starting connect the server...")

            client.connect(options, null, object : IMqttActionListener {
                override fun onSuccess(asyncActionToken: IMqttToken?) {
                    Log.d("API", "Connection success")

                    client.subscribe("/oneM2M/req/$cse/$ae/$container/$subscribe/json", 0, null, object : IMqttActionListener {
                        override fun onSuccess(asyncActionToken: IMqttToken?) {
                            Log.d("API", "Subscribed")
                        }

                        override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                            Log.d("API", "Failed to subscribe")
                        }
                    })
                }

                override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                    Log.d("API", "Connection failure")
                }
            })

            client.setCallback(this)
        } catch (error: MqttException) {
            error.printStackTrace()
        } catch (err: Exception) {
            err.printStackTrace()
        }
    }
}
