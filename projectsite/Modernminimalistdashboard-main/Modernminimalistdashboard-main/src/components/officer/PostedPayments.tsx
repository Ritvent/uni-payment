import { Eye, Search } from 'lucide-react';
import { useState } from 'react';

interface PostedPayment {
  id: string;
  date: string;
  studentId: string;
  studentName: string;
  organization: string;
  feeType: string;
  amount: number;
  orNumber: string;
  postedBy: string;
}

const mockPayments: PostedPayment[] = [
  {
    id: '1',
    date: '2024-11-25',
    studentId: '2023-00124',
    studentName: 'Sarah Chen',
    organization: 'Computer Science Society',
    feeType: 'Membership Fee',
    amount: 500,
    orNumber: 'OR-2024-001234',
    postedBy: 'Officer Chen'
  },
  {
    id: '2',
    date: '2024-11-25',
    studentId: '2023-00456',
    studentName: 'John Doe',
    organization: 'Engineering Club',
    feeType: 'Event Registration',
    amount: 350,
    orNumber: 'OR-2024-001235',
    postedBy: 'Officer Chen'
  },
  {
    id: '3',
    date: '2024-11-24',
    studentId: '2023-00789',
    studentName: 'Jane Smith',
    organization: 'Mathematics Society',
    feeType: 'Annual Dues',
    amount: 600,
    orNumber: 'OR-2024-001236',
    postedBy: 'Officer Chen'
  }
];

export function PostedPayments() {
  const [searchTerm, setSearchTerm] = useState('');
  const [payments] = useState<PostedPayment[]>(mockPayments);

  const filteredPayments = payments.filter(
    (payment) =>
      payment.studentName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      payment.studentId.includes(searchTerm) ||
      payment.orNumber.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="bg-white rounded-lg border border-gray-200">
      <div className="p-6 border-b border-gray-200">
        <h3 className="text-gray-900 mb-4">Posted Payments</h3>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search by student name, ID, or OR number..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-gray-900">Date</th>
              <th className="px-6 py-3 text-left text-gray-900">Student ID</th>
              <th className="px-6 py-3 text-left text-gray-900">Student Name</th>
              <th className="px-6 py-3 text-left text-gray-900">Organization</th>
              <th className="px-6 py-3 text-left text-gray-900">Fee Type</th>
              <th className="px-6 py-3 text-left text-gray-900">Amount</th>
              <th className="px-6 py-3 text-left text-gray-900">OR Number</th>
              <th className="px-6 py-3 text-left text-gray-900">Posted By</th>
              <th className="px-6 py-3 text-left text-gray-900">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredPayments.map((payment) => (
              <tr key={payment.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-gray-900">
                  {new Date(payment.date).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                  })}
                </td>
                <td className="px-6 py-4 text-gray-700">{payment.studentId}</td>
                <td className="px-6 py-4 text-gray-700">{payment.studentName}</td>
                <td className="px-6 py-4 text-gray-700">{payment.organization}</td>
                <td className="px-6 py-4 text-gray-700">{payment.feeType}</td>
                <td className="px-6 py-4 text-gray-900">₱{payment.amount.toFixed(2)}</td>
                <td className="px-6 py-4 text-gray-700">{payment.orNumber}</td>
                <td className="px-6 py-4 text-gray-700">{payment.postedBy}</td>
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
