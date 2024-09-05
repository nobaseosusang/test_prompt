// src/App.js
import React, { useState, useEffect } from 'react';

function App() {
  const [fraudType, setFraudType] = useState('');
  const [conversation, setConversation] = useState('');
  const [analysisResult, setAnalysisResult] = useState('');
  const [servicePrompt, setServicePrompt] = useState('');
  const [newPrompt, setNewPrompt] = useState('');
  const [fraudList, setFraudList] = useState([]);

  useEffect(() => {
    fetchFraudTypes();
    fetchServicePrompt();
  }, []);

  // 사기 유형 추가
  const addFraudType = () => {
    const socket = new WebSocket('ws://localhost:8000/api/ws/add_fraud_type');

    socket.onopen = () => {
      socket.send(JSON.stringify({ type: fraudType }));
    };

    socket.onmessage = (event) => {
      alert(event.data);
      setFraudType('');
      fetchFraudTypes();
    };

    socket.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };
  };

  // 사기 유형 삭제
  const deleteFraudType = (type) => {
    const socket = new WebSocket('ws://localhost:8000/api/ws/delete_fraud_type');

    socket.onopen = () => {
      socket.send(JSON.stringify({ type }));
    };

    socket.onmessage = (event) => {
      alert(event.data);
      fetchFraudTypes();
    };

    socket.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };
  };

  // 사기 유형 목록 가져오기
  const fetchFraudTypes = () => {
    const socket = new WebSocket('ws://localhost:8000/api/ws/get_fraud_types');

    socket.onopen = () => {
      console.log('Fetching fraud types...');
    };

    socket.onmessage = (event) => {
      setFraudList(JSON.parse(event.data));
    };

    socket.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };
  };

  // 서비스 프롬프트 변경
  const updatePrompt = () => {
    const socket = new WebSocket('ws://localhost:8000/api/ws/update_prompt');

    socket.onopen = () => {
      socket.send(JSON.stringify({ prompt: newPrompt }));
    };

    socket.onmessage = (event) => {
      alert(event.data);
      setNewPrompt('');
      fetchServicePrompt();
    };

    socket.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };
  };

  // 서비스 프롬프트 확인
  const fetchServicePrompt = () => {
    const socket = new WebSocket('ws://localhost:8000/api/ws/get_prompt');

    socket.onopen = () => {
      console.log('Fetching current prompt...');
    };

    socket.onmessage = (event) => {
      setServicePrompt(event.data);
    };

    socket.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };
  };

  // 대화 분석 요청
  const analyzeConversation = () => {
    const socket = new WebSocket('ws://localhost:8000/api/ws/analyze_conversation');

    socket.onopen = () => {
      socket.send(JSON.stringify({ conversation }));
    };

    socket.onmessage = (event) => {
      setAnalysisResult(event.data);
    };

    socket.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };
  };

  return (
    <div>
      <h1>사기 유형 관리 및 대화 분석</h1>

      <section>
        <h2>현재 프롬프트</h2>
        <p>{servicePrompt}</p>
        <textarea
          style={{ width: '100%', height: '100px', padding: '10px', fontSize: '16px' }}
          value={newPrompt}
          onChange={(e) => setNewPrompt(e.target.value)}
          placeholder="새 프롬프트 입력"
        ></textarea>
        <button onClick={updatePrompt}>프롬프트 업데이트</button>
        <button onClick={fetchServicePrompt}>현재 프롬프트 확인</button>
      </section>

      <section>
        <h2>사기 유형 추가</h2>
        <input
          type="text"
          style={{ width: '100%', padding: '10px', fontSize: '16px', marginBottom: '10px' }}
          value={fraudType}
          onChange={(e) => setFraudType(e.target.value)}
          placeholder="사기 유형 입력"
        />
        <button onClick={addFraudType}>사기 유형 추가</button>

        <h3>사기 유형 목록</h3>
        <button onClick={fetchFraudTypes}>사기 유형 확인</button>
        <ul>
          {fraudList.map((type, index) => (
            <li key={index}>
              {type}{' '}
              <button onClick={() => deleteFraudType(type)} style={{ marginLeft: '10px' }}>
                삭제
              </button>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>대화 분석</h2>
        <textarea
          style={{ width: '100%', height: '150px', padding: '10px', fontSize: '16px' }}
          value={conversation}
          onChange={(e) => setConversation(e.target.value)}
          placeholder="분석할 대화 입력"
        ></textarea>
        <button onClick={analyzeConversation}>대화 분석하기</button>

        <h3>분석 결과</h3>
        <p>{analysisResult}</p>
      </section>
    </div>
  );
}

export default App;
