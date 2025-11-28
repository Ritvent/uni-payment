import { useState } from 'react';
import { StudentDashboard } from './components/StudentDashboard';
import { OfficerDashboard } from './components/OfficerDashboard';

export default function App() {
  const [userRole, setUserRole] = useState<'student' | 'officer'>('student');
  
  // Mock user data - student with officer privileges
  const user = {
    hasOfficerProfile: true,
    studentInfo: {
      name: 'Sarah Chen',
      studentId: '2023-00124',
      program: 'BS Computer Science',
      year: '3rd Year',
      email: 'sarah.chen@university.edu',
      profilePicture: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop'
    },
    officerInfo: {
      name: 'Sarah Chen',
      position: 'Finance Officer',
      organization: 'Computer Science Society',
      accessLevel: 'Department Level'
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {userRole === 'student' ? (
        <StudentDashboard 
          user={user} 
          onSwitchToOfficer={() => setUserRole('officer')}
        />
      ) : (
        <OfficerDashboard 
          user={user} 
          onSwitchToStudent={() => setUserRole('student')}
        />
      )}
    </div>
  );
}
