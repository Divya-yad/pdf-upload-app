import { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState('');

  const API_URL = import.meta.env.VITE_API_URL;

  // Fetch uploaded PDFs from the backend
  const fetchFiles = async () => {
    try {
      const res = await axios.get(`${API_URL}/list`);
      setFiles(res.data);
    } catch (err) {
      setMessage('Error fetching files: ' + err.message);
    }
  };

  useEffect(() => {
    if (!API_URL) {
      console.error("VITE_API_URL is not defined in your .env file");
      setMessage("API configuration error. Please check .env setup.");
      return;
    }
    fetchFiles();
  }, []);

  // Handle PDF file upload
  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`${API_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setMessage(res.data.message);
      fetchFiles();
      setFile(null);
      e.target.reset();
    } catch (err) {
      const backendMsg = err?.response?.data?.detail;
      setMessage('Error uploading file: ' + (backendMsg || err.message));
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold text-center mb-4">PDF Upload/Download</h1>

      <form onSubmit={handleUpload} className="mb-4 flex justify-center">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="border p-2 mr-2"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Upload
        </button>
      </form>

      {message && <p className="text-center text-red-500">{message}</p>}

      <h2 className="text-xl font-semibold mb-2">Uploaded PDFs</h2>
      <ul className="list-disc pl-5">
        {files.map((file) => (
          <li key={file.object_key}>
            <a
              href={`${API_URL}/download/${file.object_key}`}
              className="text-blue-500 hover:underline"
              download
            >
              {file.filename}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
