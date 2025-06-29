// src/App.js
import React, { useState, useEffect } from "react";
import { AudioRecorder } from "react-audio-voice-recorder";   // already working
import axios from "axios";
import "chart.js/auto";                                       // make sure chart.js is installed
import "./index.css";                                         // Tailwind (directives live here)

/* ────────────────────────────────────────────
   SafeVoice – Dashboard-style React frontend
────────────────────────────────────────────── */
export default function App() {
  /* ••• STATE ••• */
  const [audioFile, setAudioFile]      = useState(null);
  const [blobURL,   setBlobURL]        = useState("");
  const [recording, setRecording]      = useState(false);
  const [analyzing, setAnalyzing]      = useState(false);
  const [result,    setResult]         = useState(null);

  /* ••• HELPERS ••• */
  const handleFile = (e) => {
    setAudioFile(e.target.files[0]);
    setBlobURL("");
    setResult(null);
  };

  const onStop = (blob) => {
    const file = new File([blob], "recorded_audio.wav", { type: "audio/wav" });
    setAudioFile(file);
    setBlobURL(URL.createObjectURL(blob));
  };

  const analyze = async () => {
    if (!audioFile) return;
    setAnalyzing(true);
    const fd = new FormData();
    fd.append("audio", audioFile);
    try {
      const { data } = await axios.post("http://127.0.0.1:5000/analyze", fd, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("❌ Analysis failed - check backend.");
    } finally {
      setAnalyzing(false);
    }
  };

  /* ••• DRAW PIE ONCE RESULT ARRIVES ••• */
  useEffect(() => {
    if (!result?.emotions?.all) return;
    const { all } = result.emotions;
    const labels = Object.keys(all);
    const values = Object.values(all);
    const ctx    = document.getElementById("pie");
    if (!ctx) return;
    // eslint-disable-next-line no-undef
    new Chart(ctx, {
      type: "pie",
      data: {
        labels,
        datasets: [{ data: values, backgroundColor: [
          "#14b8a6","#0ea5e9","#f97316","#f43f5e","#a855f7","#eab308","#64748b"
        ]}],
      },
      options: { plugins: { legend: { position: "right", labels:{color:"#cbd5e1"} } } },
    });
  }, [result]);

  /* ••• DASHBOARD LAYOUT ••• */
  return (
    <div className="min-h-screen flex bg-gray-900 text-slate-200">
      {/* ────────── Sidebar ────────── */}
      <aside className="hidden md:flex flex-col w-60 bg-gray-800/70 border-r border-gray-700">
        <h1 className="text-2xl font-extrabold text-center py-6 text-teal-400">
          SafeVoice
        </h1>
        <nav className="flex-1 px-4 space-y-2 text-sm">
          <a href="#input"   className="block py-2 px-3 rounded hover:bg-gray-700">🎙️ Analyze</a>
          <a href="#results" className="block py-2 px-3 rounded hover:bg-gray-700">📊 Results</a>
          <a href="#help"    className="block py-2 px-3 rounded hover:bg-gray-700">🆘 Help</a>
        </nav>
        <p className="py-4 text-center text-xs text-gray-500">
          © {new Date().getFullYear()} SafeVoice
        </p>
      </aside>

      {/* ────────── Main content ────────── */}
      <main className="flex-1 px-4 md:px-8 lg:px-12 py-10 space-y-10">
        {/* INPUT CARD */}
        <section id="input" className="bg-gray-800/60 rounded-lg p-6 shadow">
          <h2 className="text-xl font-semibold text-teal-300 mb-4">
            1️⃣ Provide Audio
          </h2>

          {/* Upload & Recorder grid */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* FILE UPLOAD */}
            <div>
              <label className="block mb-2 text-sm">Upload a file</label>
              <input type="file" accept="audio/*" onChange={handleFile} />
            </div>

            {/* RECORDER */}
            <div className="flex flex-col items-center">
              <AudioRecorder
                onRecordingComplete={onStop}
                audioTrackConstraints={{ noiseSuppression: true, echoCancellation: true }}
                showVisualizer
                downloadOnSavePress={false}
                downloadFileExtension="wav"
                className="w-full"
              />
            </div>
          </div>

          {/* PLAYBACK */}
          {blobURL && (
            <div className="mt-4">
              <p className="text-xs text-gray-400 mb-1">Playback</p>
              <audio src={blobURL} controls className="w-full" />
            </div>
          )}

          {/* ANALYZE BTN */}
          <button
            onClick={analyze}
            disabled={!audioFile || analyzing}
            className="mt-6 w-full bg-teal-600 hover:bg-teal-700 py-2 rounded transition disabled:bg-gray-600"
          >
            {analyzing ? "⚙️ Analyzing…" : "🚀 Analyze Audio"}
          </button>
        </section>

        {/* RESULTS */}
        {result && (
          <>
            {/* SUMMARY CARDS */}
            <section
              id="results"
              className="grid md:grid-cols-2 gap-6"
            >
              <Card
                title="2️⃣ Overall Emotion"
                value={result.emotions.top.label}
                score={result.emotions.top.score}
              />
              <Card
                title="3️⃣ Overall Abuse"
                value={result.abuse.label}
                score={result.abuse.score}
              />
            </section>

            {/* TRANSCRIPT & PIE */}
            <section className="grid md:grid-cols-2 gap-6">
              <div className="bg-gray-800/60 rounded-lg p-6 shadow overflow-y-auto">
                <h3 className="text-teal-300 font-semibold mb-3">4️⃣ Transcript</h3>
                <p className="whitespace-pre-wrap leading-relaxed text-sm">
                  {result.transcript}
                </p>
              </div>

              <div className="bg-gray-800/60 rounded-lg p-6 shadow flex flex-col items-center">
                <h3 className="text-teal-300 font-semibold mb-3">
                  Emotion Distribution
                </h3>
                <canvas id="pie" className="max-w-[260px]" />
              </div>
            </section>

            {/* SENTENCE TABLE */}
            <section className="bg-gray-800/60 rounded-lg p-6 shadow overflow-x-auto">
              <h3 className="text-teal-300 font-semibold mb-4">
                5️⃣ Sentence-level Details
              </h3>
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-700 text-left">
                    <th className="p-2">Sentence</th>
                    <th className="p-2">Abuse</th>
                    <th className="p-2">Top 3 Emotions</th>
                  </tr>
                </thead>
                <tbody>
                  {result.detailed_analysis.map((row, i) => (
                    <tr key={i} className="border-b border-gray-700">
                      <td className="p-2">{row.sentence}</td>
                      <td className="p-2">
                        {row.abuse.label} ({(row.abuse.score * 100).toFixed(1)}%)
                      </td>
                      <td className="p-2">
                        {row.emotions
                          .slice(0, 3)
                          .map(
                            (e) => `${e.label} (${(e.score * 100).toFixed(1)}%)`
                          )
                          .join(", ")}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>

            {/* HELP SECTION */}
            <section id="help" className="grid md:grid-cols-2 gap-6">
              <HelpCard
                title="6️⃣ Emergency Numbers"
                rows={[
                  ["USA", "911"],
                  ["India", "100 / 1091"],
                  ["UK", "999"],
                  ["Canada", "911"],
                  ["Australia", "000"],
                  ["Germany", "112 / 110"],
                  ["France", "112 / 15"],
                  ["Brazil", "190 / 192"],
                  ["South Africa", "10111 / 10177"],
                  ["Japan", "110 / 119"],
                ]}
                isPhone
              />

              <HelpCard
                title="7️⃣ Email Support"
                rows={[
                  ["USA", "support@usahelpline.org"],
                  ["India", "support@indiahelp.in"],
                  ["UK", "help@ukrescue.org"],
                  ["Canada", "support@canadaaid.ca"],
                  ["Australia", "help@ausassist.au"],
                  ["Germany", "support@germanysafety.de"],
                  ["France", "help@frsos.fr"],
                  ["Brazil", "support@brsafe.org.br"],
                  ["South Africa", "help@sahelp.co.za"],
                  ["Japan", "support@jphelpline.jp"],
                ]}
              />
            </section>
          </>
        )}
      </main>
    </div>
  );
}

/* ────────── Small reusable components ────────── */
function Card({ title, value, score }) {
  return (
    <div className="bg-gray-800/60 rounded-lg p-6 shadow">
      <h3 className="text-teal-300 font-semibold mb-2">{title}</h3>
      <p className="text-2xl font-bold">{value}</p>
      <p className="text-gray-400 text-sm">
        Score: {(score * 100).toFixed(1)}%
      </p>
    </div>
  );
}

function HelpCard({ title, rows, isPhone = false }) {
  return (
    <div className="bg-gray-800/60 rounded-lg p-6 shadow">
      <h3 className="text-teal-300 font-semibold mb-3">{title}</h3>
      <ul className="space-y-1 text-sm leading-6">
        {rows.map(([label, val]) => (
          <li key={label}>
            {isPhone ? "📞" : "📧"} {label}:{" "}
            <a
              href={isPhone ? `tel:${val.replace(/\D/g, "")}` : `mailto:${val}`}
              className="text-teal-400"
            >
              {val}
            </a>
          </li>
        ))}
      </ul>
      {!isPhone && (
        <p className="mt-2 text-xs text-gray-400">
          Attach <code>recorded_audio.wav</code> when sending.
        </p>
      )}
    </div>
  );
}
