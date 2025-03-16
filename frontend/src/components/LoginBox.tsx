import { useState, useCallback } from '@lynx-js/react';
import './LoginBox.css';

export function LoginBox() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleUsernameChange = useCallback((e) => {
    setUsername(e.target.value);
  }, []);

  const handlePasswordChange = useCallback((e) => {
    setPassword(e.target.value);
  }, []);

  const handleSubmit = useCallback(() => {
    console.log('Login attempt with:', { username, password });
    // Handle login logic here
  }, [username, password]);

  return (
    <view className="LoginBox">
      <text className="LoginBox__Title">Login</text>
      <input
        className="LoginInput"
        type="text"
        placeholder="Username"
        value={username}
        onInput={handleUsernameChange}
      />
      <input
        className="LoginInput"
        type="password"
        placeholder="Password" 
        value={password}
        onInput={handlePasswordChange}
      />
      <button 
        className="LoginButton"
        bindtap={handleSubmit}
      >
        Login
      </button>
    </view>
  );
}


