import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './Chatbot.css';
import logo from '../../assets/logo.png';
import { FaRegUserCircle } from "react-icons/fa";
import { IoAttach } from "react-icons/io5";


const Chatbot = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [file, setFile] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  const messagesEndRef = useRef(null);

  const chatWithGPT3 = async (userInput) => {
    const apiEndpoint = 'http://127.0.0.1:5000/chat';
    try {
      const response = await axios.post(apiEndpoint, { question: userInput });
      console.log(response.data.intentRecognised);
      return response.data.exchangeReply;
    } catch (error) {
      console.error('Error communicating with the API:', error.message);
      return 'Oops! Something went wrong. Please try again later.';
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() && !file) return;

    if (input.trim()) {

      const userMessage = { text: input, user: true };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      const aiMessage = { text: '...', user: false };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);
      const response = await chatWithGPT3(input);
      const newAiMessage = { text: response, user: false };
      setMessages((prevMessages) => [...prevMessages.slice(0, -1), newAiMessage]);
      setInput('');

    } else if (file) {
      const imageMessage = { text: `Uploaded image: ${file.name}`, image: previewImage, user: true };
      const botMessage = { text: "I don't have the capacity to read images yet", user: false };
      setMessages((prevMessages) => [...prevMessages, imageMessage, botMessage]);
      setFile(null);
      setPreviewImage(null);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setPreviewImage(URL.createObjectURL(selectedFile));
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chatbot-container">
      <div className="chatbot-messages">
        {messages.map((message, index) => (
          <div key={index} className='message-container'>
            {/* AI logo for AI message */}
            <div className='aiLogo' style={{ display: message.user ? 'none' : 'flex' }}>
              <img style={{ width: '100%' }} src={logo} alt="logo" />
            </div>
            <div className={`message ${message.user ? 'user-message' : 'ai-message'}`}
                 style={{ justifyContent: message.image ? 'center' : 'flex-end' }}
            >
              {!message.image && message.text}
              {message.image && <img style={{ width: '100%' }} src={message.image} alt="Uploaded" className="uploaded-image" />}
            </div>
            {/* User logo for user message */}
            <div className='userLogo' style={{ display: message.user ? 'flex' : 'none' }}>
              <FaRegUserCircle style={{ fontSize: 'xx-large' }} />
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
        {messages.length === 0 && (
          <div style={{ display: 'flex', justifyContent: 'center' }} className="message">
            <p> <b>Welcome to CXAPP Chatbot. Ask me anything.</b> </p>
          </div>
        )}
      </div>
      <form className="chatbot-input-form" onSubmit={handleSubmit}>
        <div className={ previewImage ? `image-preview-container` : ``}>
          {previewImage && <img src={previewImage} alt="Preview" className="preview-image" />}
        </div>
        <div className="input-container">
          <input type="text" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Type your message..." />
          <label htmlFor="file-input" className="file-upload-label">
            <IoAttach />
          </label>
          <input id="file-input" type="file" onChange={handleFileChange} accept="image/*" style={{ display: 'none' }} />
          <button type="submit">Send</button>
        </div>
      </form>
    </div>
  );
};

export default Chatbot;