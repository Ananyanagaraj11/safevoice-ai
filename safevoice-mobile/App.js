import React, { useState } from 'react';
import { View, Button, Text, StyleSheet, ScrollView } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import axios from 'axios';

export default function App() {
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState('');

  const pickAudio = async () => {
    setError('');
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: 'audio/*',
        copyToCacheDirectory: true,
      });

      if (result.type === 'success') {
        const formData = new FormData();
        formData.append('file', {
          uri: result.uri,
          name: result.name,
          type: 'audio/mpeg',
        });

        const response = await axios.post('http://192.168.1.194:5000/analyze', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        setAnalysis(response.data);
      }
    } catch (err) {
      setError('Error uploading or analyzing audio.');
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>🎤 SafeVoice Mobile</Text>
      <Button title="Upload Voice Clip" onPress={pickAudio} />
      {error !== '' && <Text style={styles.error}>{error}</Text>}
      {analysis && (
        <View style={styles.result}>
          <Text style={styles.subtitle}>Summary: {analysis.summary}</Text>
          <Text>Detected Emotions:</Text>
          {Object.entries(analysis.emotion_distribution).map(([emotion, value]) => (
            <Text key={emotion}>- {emotion}: {value}</Text>
          ))}
          <Text style={styles.subtitle}>Abuse Analysis:</Text>
          {analysis.sentence_analysis.map((item, index) => (
            <Text key={index}>
              "{item.sentence}" → Emotion: {item.emotion}, Abuse: {item.abuse}
            </Text>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 20,
    justifyContent: 'flex-start',
    backgroundColor: '#f0f4f8',
  },
  title: {
    fontSize: 26,
    fontWeight: 'bold',
    marginVertical: 20,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 18,
    marginTop: 15,
    fontWeight: '600',
  },
  result: {
    marginTop: 20,
    padding: 10,
    backgroundColor: '#fff',
    borderRadius: 8,
  },
  error: {
    marginTop: 10,
    color: 'red',
  },
});

