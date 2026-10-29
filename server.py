from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

jobs = [
    {
        'id': 1,
        'title': 'Delivery Partner',
        'company': 'Work Vaib Sample Co.',
        'location': 'Mumbai',
        'salary': '₹15,000 - ₹25,000/month',
        'contact': 'hr@sample.com',
        'approved': True,
        'description': 'Deliver parcels in your area. License required.'
    }
]

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    approved_jobs = [j for j in jobs if j['approved']]
    return jsonify(approved_jobs)

@app.route('/api/jobs', methods=['POST'])
def post_job():
    data = request.json
    new_job = {
        'id': len(jobs) + 1,
        'title': data.get('title'),
        'company': data.get('company'),
        'location': data.get('location'),
        'salary': data.get('salary'),
        'contact': data.get('contact'),
        'description': data.get('description'),
        'approved': False
    }
    jobs.append(new_job)
    return jsonify({'message': 'Job submitted for admin approval', 'job': new_job}), 201

@app.route('/api/admin/jobs', methods=['GET'])
def admin_get_jobs():
    return jsonify(jobs)

@app.route('/api/admin/approve/<int:job_id>', methods=['POST'])
def approve_job(job_id):
    for job in jobs:
        if job['id'] == job_id:
            job['approved'] = True
            return jsonify({'message': 'Job approved successfully', 'job': job})
    return jsonify({'error': 'Job not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)

// src/App.js (Frontend)
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [view, setView] = useState('jobs');
  const [newJob, setNewJob] = useState({ title: '', company: '', location: '', salary: '', contact: '', description: '' });
  const [adminJobs, setAdminJobs] = useState([]);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = () => {
    fetch('http://localhost:5000/api/jobs')
      .then(res => res.json())
      .then(data => setJobs(data));
  };

  const fetchAdminJobs = () => {
    fetch('http://localhost:5000/api/admin/jobs')
      .then(res => res.json())
      .then(data => setAdminJobs(data));
  };

  const handlePostJob = (e) => {
    e.preventDefault();
    fetch('http://localhost:5000/api/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newJob)
    }).then(() => {
      alert('Job posted! Waiting for Admin approval.');
      setNewJob({ title: '', company: '', location: '', salary: '', contact: '', description: '' });
      setView('jobs');
    });
  };

  const handleApprove = (id) => {
    fetch(`http://localhost:5000/api/admin/approve/${id}`, { method: 'POST' })
      .then(() => {
        fetchAdminJobs();
        fetchJobs();
      });
  };

  return (
    <div className="App">
      <header className="navbar">
        <h1>Work Vaib</h1>
        <p>Find a real job. Hire for free. <strong>No fraud.</strong></p>
        <nav>
          <button onClick={() => setView('jobs')}>Find Jobs</button>
          <button onClick={() => setView('post')}>Post a Job (Free)</button>
          <button onClick={() => { setView('admin'); fetchAdminJobs(); }}>Admin Panel</button>
        </nav>
      </header>

      {view === 'jobs' && (
        <main className="job-list">
          <h2>Available Jobs</h2>
          {jobs.map(job => (
            <div key={job.id} className="job-card">
              <h3>{job.title}</h3>
              <p><strong>Company:</strong> {job.company}</p>
              <p><strong>Location:</strong> {job.location} | <strong>Salary:</strong> {job.salary}</p>
              <p>{job.description}</p>
              <p className="contact"><strong>Contact to Apply:</strong> {job.contact}</p>
            </div>
          ))}
        </main>
      )}

      {view === 'post' && (
        <main className="form-container">
          <h2>Post a Free Job</h2>
          <form onSubmit={handlePostJob}>
            <input placeholder="Job Title" value={newJob.title} onChange={e => setNewJob({...newJob, title: e.target.value})} required />
            <input placeholder="Company Name" value={newJob.company} onChange={e => setNewJob({...newJob, company: e.target.value})} required />
            <input placeholder="Location" value={newJob.location} onChange={e => setNewJob({...newJob, location: e.target.value})} required />
            <input placeholder="Salary Range" value={newJob.salary} onChange={e => setNewJob({...newJob, salary: e.target.value})} required />
            <input placeholder="Contact Email / Phone" value={newJob.contact} onChange={e => setNewJob({...newJob, contact: e.target.value})} required />
            <textarea placeholder="Job Description" value={newJob.description} onChange={e => setNewJob({...newJob, description: e.target.value})} required />
            <button type="submit">Submit Job</button>
          </form>
        </main>
      )}

      {view === 'admin' && (
        <main className="admin-panel">
          <h2>Admin Job Verification</h2>
          {adminJobs.map(job => (
            <div key={job.id} className="job-card">
              <h3>{job.title} ({job.company})</h3>
              <p>Status: {job.approved ? 'Approved' : 'Pending Approval'}</p>
              {!job.approved && (
                <button onClick={() => handleApprove(job.id)}>Approve Job</button>
              )}
            </div>
          ))}
        </main>
      )}
    </div>
  );
}

export default App;

/* App.css */
body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
.navbar { display: flex; flex-direction: column; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 15px; }
.navbar nav button { margin: 5px; padding: 8px 16px; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer; }
.job-list, .form-container, .admin-panel { max-width: 600px; margin: 20px auto; }
.job-card { background: #1e293b; border: 1px solid #334155; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
.contact { color: #38bdf8; font-weight: bold; }
form { display: flex; flex-direction: column; gap: 10px; }
input, textarea { padding: 10px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 4px; }
button[type='submit'] { padding: 10px; background: #16a34a; color: white; border: none; border-radius: 4px; cursor: pointer; }

