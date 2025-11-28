import { useState } from 'react';
import { ProfileDropdown } from './ProfileDropdown';
import { OrganizationFeesTable } from './OrganizationFeesTable';
import { TransactionHistoryTable } from './TransactionHistoryTable';
import { Toggle } from './ui/Toggle';

interface StudentDashboardProps {
  user: any;
  onSwitchToOfficer: () => void;
}

export function StudentDashboard({ user, onSwitchToOfficer }: StudentDashboardProps) {
  const [activeTab, setActiveTab] = useState<'fees' | 'transactions'>('fees');

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
        {/* Hero Section */}
        <div className="bg-white rounded-lg border border-gray-200 p-8 mb-6">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-gray-900 mb-2">Welcome back, {user.studentInfo.name}</h2>
              <div className="space-y-1">
                <p className="text-gray-600">Student ID: {user.studentInfo.studentId}</p>
                <p className="text-gray-600">{user.studentInfo.program} • {user.studentInfo.year}</p>
                <p className="text-gray-600">{user.studentInfo.email}</p>
              </div>
            </div>
            {user.hasOfficerProfile && (
              <button
                onClick={onSwitchToOfficer}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Switch to Officer View
              </button>
            )}
          </div>
        </div>

        {/* Toggle Tabs */}
        <div className="mb-6">
          <div className="inline-flex bg-white border border-gray-200 rounded-lg p-1">
            <button
              onClick={() => setActiveTab('fees')}
              className={`px-6 py-2 rounded-md transition-colors ${
                activeTab === 'fees'
                  ? 'bg-gray-900 text-white'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Organization Fees
            </button>
            <button
              onClick={() => setActiveTab('transactions')}
              className={`px-6 py-2 rounded-md transition-colors ${
                activeTab === 'transactions'
                  ? 'bg-gray-900 text-white'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Transactions
            </button>
          </div>
        </div>

        {/* Content Area */}
        {activeTab === 'fees' ? (
          <OrganizationFeesTable />
        ) : (
          <TransactionHistoryTable />
        )}
      </main>
    </div>
  );
}
