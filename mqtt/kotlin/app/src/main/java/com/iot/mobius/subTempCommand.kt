package com.iot.mobius

import android.content.Context
import android.util.Log
import com.iot.api.MQTT

fun subTempCommand(context: Context) {
    val recv: (String) -> Unit = { response ->
        Log.d("API", "$response")
    }

    val mqtt = MQTT()

    // temp_sensor(AE-ID) temp_command(컨테이너)에 temp_sub 구독을 요청한다.
    mqtt.connect(context, recv, "ae_test", "cnt_test", "sub_test");
}