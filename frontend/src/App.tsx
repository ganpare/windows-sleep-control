import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// APIのベースURL
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

// Windowsのステータスタイプ
type WindowsStatus = 'awake' | 'sleep' | 'unknown' | 'loading';

function App() {
  // Windowsのステータス
  const [status, setStatus] = useState<WindowsStatus>('loading');
  // API呼び出し中かどうか
  const [loading, setLoading] = useState<boolean>(false);
  // エラーメッセージ
  const [error, setError] = useState<string | null>(null);

  // ページ読み込み時にステータスを取得
  useEffect(() => {
    fetchStatus();
    // 30秒ごとにステータスを更新
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  // ステータスを取得する関数
  const fetchStatus = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/status`);
      setStatus(response.data.status);
      setError(null);
    } catch (err) {
      console.error('ステータス取得エラー:', err);
      setStatus('unknown');
      setError('サーバーに接続できませんでした');
    } finally {
      setLoading(false);
    }
  };

  // スリープさせる関数
  const handleSleep = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/sleep`);
      if (response.data.success) {
        setStatus('sleep');
      }
      setError(null);
    } catch (err) {
      console.error('スリープエラー:', err);
      setError('スリープ処理中にエラーが発生しました');
    } finally {
      setLoading(false);
    }
  };

  // 起動させる関数
  const handleWake = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/wake`);
      if (response.data.success) {
        // Wake-on-LANパケット送信後、少し待ってからステータスを再取得
        setTimeout(fetchStatus, 5000);
      }
      setError(null);
    } catch (err) {
      console.error('起動エラー:', err);
      setError('起動処理中にエラーが発生しました');
    } finally {
      setLoading(false);
    }
  };

  // ステータスに応じたアイコンとテキストを取得
  const getStatusInfo = () => {
    switch (status) {
      case 'awake':
        return {
          icon: '🟢',
          text: '起動中',
          description: 'Windowsマシンは起動しています'
        };
      case 'sleep':
        return {
          icon: '💤',
          text: 'スリープ中',
          description: 'Windowsマシンはスリープ状態です'
        };
      case 'loading':
        return {
          icon: '⏳',
          text: '読み込み中',
          description: 'ステータスを確認しています...'
        };
      default:
        return {
          icon: '❓',
          text: '不明',
          description: 'Windowsマシンの状態を確認できません'
        };
    }
  };

  const statusInfo = getStatusInfo();

  return (
    <div className="App">
      <header className="App-header">
        <h1>Windows スリープ/復帰コントロール</h1>
      </header>
      
      <main className="App-main">
        <div className="status-container">
          <div className="status-icon">{statusInfo.icon}</div>
          <h2 className="status-text">{statusInfo.text}</h2>
          <p className="status-description">{statusInfo.description}</p>
        </div>

        {error && <div className="error-message">{error}</div>}
        
        <div className="button-container">
          <button 
            className="action-button sleep-button"
            onClick={handleSleep}
            disabled={loading || status === 'sleep'}
          >
            スリープ
          </button>
          
          <button 
            className="action-button wake-button"
            onClick={handleWake}
            disabled={loading || status === 'awake'}
          >
            起動
          </button>
        </div>
        
        <button 
          className="refresh-button"
          onClick={fetchStatus}
          disabled={loading}
        >
          {loading ? '更新中...' : 'ステータス更新'}
        </button>
      </main>
      
      <footer className="App-footer">
        <p> 2025 Windows スリープ/復帰コントロール</p>
      </footer>
    </div>
  );
}

export default App;
