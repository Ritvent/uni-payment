import { Eye, Download } from 'lucide-react';

interface Transaction {
  id: string;
  date: string;
  time: string;
  studentId: string;
  studentName: string;
  organization: string;
  feeType: string;
  amount: number;
  orNumber: string;
  status: 'completed' | 'pending' | 'failed';
}

const mockTransactions: Transaction[] = [
  {
    id: '1',
    date: '2024-11-25',
    time: '10:30 AM',
    studentId: '2023-00124',
    studentName: 'Sarah Chen',
    organization: 'Computer Science Society',
    feeType: 'Membership Fee',
    amount: 500,
    orNumber: 'OR-2024-001234',
    status: 'completed'
  },
  {
    id: '2',
    date: '2024-11-25',
    time: '11:15 AM',
    studentId: '2023-00456',
    studentName: 'John Doe',
    organization: 'Engineering Club',
    feeType: 'Event Registration',
    amount: 350,
    orNumber: 'OR-2024-001235',
    status: 'completed'
  },
  {
    id: '3',
    date: '2024-11-25',
    time: '02:45 PM',
    studentId: '2023-00789',
    studentName: 'Jane Smith',
    organization: 'Mathematics Society',
    feeType: 'Annual Dues',
    amount: 600,
    orNumber: 'OR-2024-001236',
    status: 'completed'
  }
];

export function OfficerTransactions() {
  const getStatusBadge = (status: Transaction['status']) => {
    const styles = {
      completed: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      failed: 'bg-red-100 text-red-800'
    };

    return (
      <span className={`px-3 py-1 rounded-full ${styles[status]}`}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200">
      <div className="p-6 border-b border-gray-200 flex items-center justify-between">
        <div>
          <h3 className="text-gray-900">Recent Transactions</h3>
          <p className="text-gray-600">All payment transactions</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors">
          <Download className="w-4 h-4" />
          Export
        </button>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-gray-900">Date & Time</th>
              <th className="px-6 py-3 text-left text-gray-900">Student ID</th>
              <th className="px-6 py-3 text-left text-gray-900">Student Name</th>
              <th className="px-6 py-3 text-left text-gray-900">Organization</th>
              <th className="px-6 py-3 text-left text-gray-900">Fee Type</th>
              <th className="px-6 py-3 text-left text-gray-900">Amount</th>
              <th className="px-6 py-3 text-left text-gray-900">OR Number</th>
              <th className="px-6 py-3 text-left text-gray-900">Status</th>
              <th className="px-6 py-3 text-left text-gray-900">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {mockTransactions.map((transaction) => (
              <tr key={transaction.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-gray-900">
                  <div>{new Date(transaction.date).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                  })}</div>
                  <div className="text-gray-600">{transaction.time}</div>
                </td>
                <td className="px-6 py-4 text-gray-700">{transaction.studentId}</td>
                <td className="px-6 py-4 text-gray-700">{transaction.studentName}</td>
                <td className="px-6 py-4 text-gray-700">{transaction.organization}</td>
                <td className="px-6 py-4 text-gray-700">{transaction.feeType}</td>
                <td className="px-6 py-4 text-gray-900">₱{transaction.amount.toFixed(2)}</td>
                <td className="px-6 py-4 text-gray-700">{transaction.orNumber}</td>
                <td className="px-6 py-4">{getStatusBadge(transaction.status)}</td>
                <td className="px-6 py-4">
                  <button className="flex items-center gap-2 px-3 py-1 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 transition-colors">
                    <Eye className="w-4 h-4" />
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
