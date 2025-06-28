import React, { useState } from "react";
import { ReactMic } from "react-mic";
import axios from "axios";
import "./App.css";

function App() {
  const [audioFile, setAudioFile] = useState(null);
  const [recording, setRecording] = useState(false);
  const [blobURL, setBlobURL] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleFileChange = (e) => {
    setAudioFile(e.target.files[0]);
    setBlobURL("");
    setAnalysisResult(null);
  };

  const startRecording = () => {
    setRecording(true);
    setAnalysisResult(null);
  };

  const stopRecording = () => {
    setRecording(false);
  };

  const onStop = (recordedBlob) => {
    setAudioFile(new File([recordedBlob.blob], "recorded_audio.wav", { type: "audio/wav" }));
    setBlobURL(recordedBlob.blobURL);
  };

  const handleAnalyze = async () => {
    if (!audioFile) return;
    setAnalyzing(true);
    const formData = new FormData();
    formData.append("audio", audioFile);

    try {
      const response = await axios.post("http://127.0.0.1:5000/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setAnalysisResult(response.data);
    } catch (error) {
      console.error("Analysis error:", error);
    } finally {
      setAnalyzing(false);
    }
  };

  const renderChart = () => {
    if (!analysisResult?.emotions?.all) return null;

    const chartData = analysisResult.emotions.all;
    const labels = Object.keys(chartData);
    const values = Object.values(chartData);

    setTimeout(() => {
      const ctx = document.getElementById("emotionChart");
      if (ctx && window.Chart) {
        new window.Chart(ctx, {
          type: "pie",
          data: {
            labels,
            datasets: [
              {
                data: values,
                backgroundColor: [
                  "#FF6384",
                  "#36A2EB",
                  "#FFCE56",
                  "#4BC0C0",
                  "#9966FF",
                  "#FF9F40",
                  "#C9CBCF",
                ],
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: "right",
              },
            },
          },
        });
      }
    }, 300);

    return (
      <div className="chart">
        <h3>4. Emotion Distribution</h3>
        <canvas id="emotionChart" width="300" height="300"></canvas>
      </div>
    );
  };

  return (
    <div className="container">
      <h1>🎙️ SafeVoice: Abuse & Emotion Detector</h1>

      <div className="upload-section">
        <input type="file" accept="audio/*" onChange={handleFileChange} />
        <p>OR</p>
        <ReactMic
          record={recording}
          className="sound-wave"
          onStop={onStop}
          strokeColor="#000000"
          backgroundColor="#f3f3f3"
        />
        <button onClick={recording ? stopRecording : startRecording}>
          {recording ? "Stop Recording" : "Start Recording"}
        </button>
      </div>

      <button onClick={handleAnalyze} disabled={!audioFile || analyzing}>
        {analyzing ? "Analyzing..." : "Analyze Audio"}
      </button>

      {blobURL && (
        <div className="player">
          <p>▶️ Playback:</p>
          <audio src={blobURL} controls />
        </div>
      )}

      {analysisResult && (
        <div className="results">
          <h2>1. Overall Emotion: {analysisResult.emotions.top.label}</h2>
          <p>Score: {(analysisResult.emotions.top.score * 100).toFixed(1)}%</p>

          <h2>2. Overall Abuse: {analysisResult.abuse.label}</h2>
          <p>Score: {(analysisResult.abuse.score * 100).toFixed(1)}%</p>

          <h2>3. Transcription</h2>
          <p>{analysisResult.transcript}</p>

          {renderChart()}

          <h2>5. Sentence-Level Analysis</h2>
          <table>
            <thead>
              <tr>
                <th>Sentence</th>
                <th>Abuse</th>
                <th>Top 3 Emotions</th>
              </tr>
            </thead>
            <tbody>
              {analysisResult.detailed_analysis.map((s, i) => (
                <tr key={i}>
                  <td>{s.sentence}</td>
                  <td>
                    {s.abuse.label} ({(s.abuse.score * 100).toFixed(1)}%)
                  </td>
                  <td>
                    {s.emotions
                      .slice(0, 3)
                      .map((e) => `${e.label} (${(e.score * 100).toFixed(1)}%)`)
                      .join(", ")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* 6. Emergency Contact Numbers */}
          <div className="section">
            <h2>6. Do You Need Help? Emergency Contact Numbers</h2>
            <ul>
              <li><strong>📞 USA:</strong> <a href="tel:911">911</a> (Emergency Services)</li>
              <li><strong>📞 India:</strong> <a href="tel:100">100</a> (Police), <a href="tel:1091">1091</a> (Women’s Helpline)</li>
              <li><strong>📞 UK:</strong> <a href="tel:999">999</a> (Emergency Services)</li>
              <li><strong>📞 Canada:</strong> <a href="tel:911">911</a> (Emergency Services)</li>
              <li><strong>📞 Australia:</strong> <a href="tel:000">000</a> (Emergency Services)</li>
              <li><strong>📞 Germany:</strong> <a href="tel:112">112</a> (Ambulance), <a href="tel:110">110</a> (Police)</li>
              <li><strong>📞 France:</strong> <a href="tel:112">112</a> (EU Emergency), <a href="tel:15">15</a> (Ambulance)</li>
              <li><strong>📞 Brazil:</strong> <a href="tel:190">190</a> (Police), <a href="tel:192">192</a> (Ambulance)</li>
              <li><strong>📞 South Africa:</strong> <a href="tel:10111">10111</a> (Police), <a href="tel:10177">10177</a> (Ambulance)</li>
              <li><strong>📞 Japan:</strong> <a href="tel:110">110</a> (Police), <a href="tel:119">119</a> (Fire/Ambulance)</li>
            </ul>
          </div>

          {/* 7. Email Support Contacts */}
          <div className="section">
            <h2>7. Email Support Contacts</h2>
            <ul>
              <li><strong>📧 USA:</strong> <a href="mailto:support@usahelpline.org?subject=Help Needed&body=Please find attached the recorded audio for support.">support@usahelpline.org</a></li>
              <li><strong>📧 India:</strong> <a href="mailto:support@indiahelp.in?subject=Assistance Request&body=Audio report attached for review.">support@indiahelp.in</a></li>
              <li><strong>📧 UK:</strong> <a href="mailto:help@ukrescue.org?subject=Urgent Help&body=Attached audio may contain abusive content.">help@ukrescue.org</a></li>
              <li><strong>📧 Canada:</strong> <a href="mailto:support@canadaaid.ca?subject=Support Request&body=Please check the attached voice note.">support@canadaaid.ca</a></li>
              <li><strong>📧 Australia:</strong> <a href="mailto:help@ausassist.au?subject=Immediate Support&body=Attached audio contains critical information.">help@ausassist.au</a></li>
              <li><strong>📧 Germany:</strong> <a href="mailto:support@germanysafety.de?subject=Support Request&body=Need help regarding the attached audio report.">support@germanysafety.de</a></li>
              <li><strong>📧 France:</strong> <a href="mailto:help@frsos.fr?subject=Aide Requise&body=Merci de vérifier l’audio ci-joint.">help@frsos.fr</a></li>
              <li><strong>📧 Brazil:</strong> <a href="mailto:support@brsafe.org.br?subject=Urgência&body=O áudio gravado está anexado para avaliação.">support@brsafe.org.br</a></li>
              <li><strong>📧 South Africa:</strong> <a href="mailto:help@sahelp.co.za?subject=Emergency Support&body=Please review the audio attached.">help@sahelp.co.za</a></li>
              <li><strong>📧 Japan:</strong> <a href="mailto:support@jphelpline.jp?subject=相談&body=録音された音声を添付しています。ご確認ください。">support@jphelpline.jp</a></li>
            </ul>
            <p><em>📎 You can manually attach the recorded audio file (<code>recorded_audio.wav</code>) while sending the email.</em></p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
