import { useState } from 'react';
import { ProfileDropdown } from './ProfileDropdown';
import { QRScanner } from './officer/QRScanner';
import { PostPayment } from './officer/PostPayment';
import { PostedPayments } from './officer/PostedPayments';
import { OfficerTransactions } from './officer/OfficerTransactions';
import { ViewStudents } from './officer/ViewStudents';
import { ViewOfficers } from './officer/ViewOfficers';
import { GenerateCode } from './officer/GenerateCode';
import { Activity, Users, DollarSign, Clock } from 'lucide-react';

interface OfficerDashboardProps {
  user: any;
  onSwitchToStudent: () => void;
}

export function OfficerDashboard({ user, onSwitchToStudent }: OfficerDashboardProps) {
  const [activeView, setActiveView] = useState<'dashboard' | 'students' | 'officers' | 'generate'>('dashboard');
  const [activeFeature, setActiveFeature] = useState<'qr' | 'post' | 'posted' | 'transactions'>('qr');

  const stats = [
    { label: 'Pending Requests', value: '12', icon: Clock, color: 'text-orange-600' },
    { label: 'Total Collected', value: '₱45,230', icon: DollarSign, color: 'text-green-600' },
    { label: "Today's Collection", value: '₱8,450', icon: Activity, color: 'text-blue-600' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-gray-900">University Payment System</h1>
            <ProfileDropdown user={user.studentInfo} />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Officer Info Section */}
        <div className="bg-white rounded-lg border border-gray-200 p-8 mb-6">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h2 className="text-gray-900 mb-2">{user.officerInfo.name}</h2>
              <p className="text-gray-600">{user.officerInfo.position}</p>
              <p className="text-gray-600">{user.officerInfo.organization}</p>
            </div>
            <button
              onClick={onSwitchToStudent}
              className="px-4 py-2 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Switch to Student View
            </button>
          </div>

          {/* Role Toggle */}
          <div className="inline-flex bg-gray-50 border border-gray-200 rounded-lg p-1 mb-6">
            <button className="px-4 py-2 rounded-md bg-gray-900 text-white">
              Officer
            </button>
            <button className="px-4 py-2 rounded-md text-gray-600">
              Student
            </button>
            <button className="px-4 py-2 rounded-md text-gray-600">
              Admin Panel
            </button>
          </div>

          {/* System Status */}
          <div className="flex items-center gap-2 mb-6">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-gray-700">System Status: Online & Active</span>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {stats.map((stat, index) => (
              <div key={index} className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center gap-3">
                  <stat.icon className={`w-5 h-5 ${stat.color}`} />
                  <div>
                    <p className="text-gray-600">{stat.label}</p>
                    <p className="text-gray-900">{stat.value}</p>
                  </div>
                </div>
              </div>
            ))}
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-600">Access Level</p>
              <p className="text-gray-900">{user.officerInfo.accessLevel}</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="mb-6">
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={() => setActiveView('dashboard')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                activeView === 'dashboard'
                  ? 'bg-gray-900 text-white'
                  : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'
              }`}
            >
              Dashboard
            </button>
            <button
              onClick={() => setActiveView('students')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                activeView === 'students'
                  ? 'bg-gray-900 text-white'
                  : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'
              }`}
            >
              View Students
            </button>
            <button
              onClick={() => setActiveView('officers')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                activeView === 'officers'
                  ? 'bg-gray-900 text-white'
                  : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'
              }`}
            >
              View Officers
            </button>
            <button
              onClick={() => setActiveView('generate')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                activeView === 'generate'
                  ? 'bg-gray-900 text-white'
                  : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'
              }`}
            >
              Generate HTML/CSS/JS
            </button>
          </div>
        </div>

        {/* Main Content Area */}
        {activeView === 'dashboard' && (
          <>
            {/* Feature Toggles */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
              <h3 className="text-gray-900 mb-4">Features</h3>
              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={() => setActiveFeature('qr')}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    activeFeature === 'qr'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  QR Scanner
                </button>
                <button
                  onClick={() => setActiveFeature('post')}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    activeFeature === 'post'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Post Payment
                </button>
                <button
                  onClick={() => setActiveFeature('posted')}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    activeFeature === 'posted'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Posted Payments
                </button>
                <button
                  onClick={() => setActiveFeature('transactions')}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    activeFeature === 'transactions'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Transactions
                </button>
              </div>
            </div>

            {/* Feature Content */}
            <div className="mb-6">
              {activeFeature === 'qr' && <QRScanner />}
              {activeFeature === 'post' && <PostPayment />}
              {activeFeature === 'posted' && <PostedPayments />}
              {activeFeature === 'transactions' && <OfficerTransactions />}
            </div>
          </>
        )}

        {activeView === 'students' && <ViewStudents />}
        {activeView === 'officers' && <ViewOfficers />}
        {activeView === 'generate' && <GenerateCode />}
      </main>
    </div>
  );
}
