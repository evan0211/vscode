using System.Collections;
using UnityEngine;  
using UnityEngine.Networking; // 使用 UnityWebRequest 需要這個命名空間
public class FlashlightController : MonoBehaviour  
{  
    private AndroidJavaObject cameraManager;  
    private string cameraId;    
    string url = "http://twasiaunivi629.ddns.net/lightcode.txt";
    string text2 = "";
    void Start()  
    {  
        // 開始協程來讀取文本
        StartCoroutine(ReadTextFromURL());
        
       
    }  
    IEnumerator ReadTextFromURL()
    {
        // 發送HTTP請求來獲取文本文件
        UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.ConnectionError || request.result == UnityWebRequest.Result.ProtocolError)
        {
            // 如果發生錯誤，打印錯誤訊息
            Debug.LogError("Error while downloading text: " + request.error);
        }
        else
        {
            // 成功讀取，打印文件內容
            text2 = request.downloadHandler.text;
            Debug.Log("text2: " + text2);
            if (Application.platform == RuntimePlatform.Android)  
            {  
                using (var activityClass = new AndroidJavaClass("com.unity3d.player.UnityPlayer"))  
                {  
                    AndroidJavaObject activity = activityClass.GetStatic<AndroidJavaObject>("currentActivity");  
                    cameraManager = activity.Call<AndroidJavaObject>("getSystemService", "camera");  
                    cameraId = cameraManager.Call<string[]>("getCameraIdList")[0];  
                }  
                
                // 开始摩尔斯密码传递  
                StartCoroutine(TransmitMorseCode(text2));  
            } 

        }
    }
    

    void Update()
    {
        
    }

    private IEnumerator TransmitMorseCode(string message)  
    {  
        foreach (char c in message)  
        {  
            switch (c)  
            {  
                case 'a':
                    yield return FlashMorse(".-");
                    break;
                case 'b':
                    yield return FlashMorse("-...");
                    break;
                case 'c':
                    yield return FlashMorse("-.-.");
                    break;
                case 'd':
                    yield return FlashMorse("-..");
                    break;
                case 'e':
                    yield return FlashMorse(".");
                    break;
                case 'f':
                    yield return FlashMorse("..-.");
                    break;
                case 'g':
                    yield return FlashMorse("--.");
                    break;
                case 'h':
                    yield return FlashMorse("....");
                    break;
                case 'i':
                    yield return FlashMorse("..");
                    break;
                case 'j':
                    yield return FlashMorse(".---");
                    break;
                case 'k':
                    yield return FlashMorse("-.-");
                    break;
                case 'l':
                    yield return FlashMorse(".-..");
                    break;
                case 'm':
                    yield return FlashMorse("--");
                    break;
                case 'n':
                    yield return FlashMorse("-.");
                    break;
                case 'o':
                    yield return FlashMorse("---");
                    break;
                case 'p':
                    yield return FlashMorse(".--.");
                    break;
                case 'q':
                    yield return FlashMorse("--.-");
                    break;
                case 'r':
                    yield return FlashMorse(".-.");
                    break;
                case 's':
                    yield return FlashMorse("...");
                    break;
                case 't':
                    yield return FlashMorse("-");
                    break;
                case 'u':
                    yield return FlashMorse("..-");
                    break;
                case 'v':
                    yield return FlashMorse("...-");
                    break;
                case 'w':
                    yield return FlashMorse(".--");
                    break;
                case 'x':
                    yield return FlashMorse("-..-");
                    break;
                case 'y':
                    yield return FlashMorse("-.--");
                    break;
                case 'z':
                    yield return FlashMorse("--..");
                    break;
                case '1':
                    yield return FlashMorse(".----");
                    break;
                case '2':
                    yield return FlashMorse("..---");
                    break;
                case '3':
                    yield return FlashMorse("...--");
                    break;
                case '4':
                    yield return FlashMorse("....-");
                    break;
                case '5':
                    yield return FlashMorse(".....");
                    break;
                case '6':
                    yield return FlashMorse("-....");
                    break;
                case '7':
                    yield return FlashMorse("--...");
                    break;
                case '8':
                    yield return FlashMorse("---..");
                    break;
                case '9':
                    yield return FlashMorse("----.");
                    break;
                case '0':
                    yield return FlashMorse("-----");
                    break;
                // 处理空格，字母之间的间隔
                case ' ':
                    yield return new WaitForSeconds(3.0f); // 单词之间的间隔更长
                    break;  
            }  
            // 字母间的间隔  
            yield return new WaitForSeconds(1.0f);  
        }  

        // 传递完成后关闭手电筒  
        SetFlashlight(false);  
    }  

    private IEnumerator FlashMorse(string morseCode)  
    {  
        foreach (char dotOrDash in morseCode)  
        {  
            if (dotOrDash == '.')  
            {  
                SetFlashlight(true);  
                yield return new WaitForSeconds(0.2f); // 短閃 
                SetFlashlight(false);  
                yield return new WaitForSeconds(0.2f); // 短閃間隔  
            }  
            else if (dotOrDash == '-')  
            {  
                SetFlashlight(true);  
                yield return new WaitForSeconds(0.6f); // 長閃  
                SetFlashlight(false);  
                yield return new WaitForSeconds(0.2f); // 短閃間隔  
            }  
        }  
    }  

    private void SetFlashlight(bool enable)  
    {  
        if (Application.platform == RuntimePlatform.Android)  
        {  
            cameraManager.Call("setTorchMode", cameraId, enable);  
        }  
    }  
}  
