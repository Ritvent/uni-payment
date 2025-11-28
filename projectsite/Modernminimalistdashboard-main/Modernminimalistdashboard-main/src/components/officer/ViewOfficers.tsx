import { Search, Mail, Shield } from 'lucide-react';
import { useState } from 'react';

interface Officer {
  id: string;
  name: string;
  position: string;
  organization: string;
  email: string;
  accessLevel: string;
  paymentsProcessed: number;
  status: 'active' | 'inactive';
}

const mockOfficers: Officer[] = [
  {
    id: '1',
    name: 'Sarah Chen',
    position: 'Finance Officer',
    organization: 'Computer Science Society',
    email: 'sarah.chen@university.edu',
    accessLevel: 'Department Level',
    paymentsProcessed: 156,
    status: 'active'
  },
  {
    id: '2',
    name: 'Michael Torres',
    position: 'Treasurer',
    organization: 'Engineering Student Council',
    email: 'michael.torres@university.edu',
    accessLevel: 'Department Level',
    paymentsProcessed: 234,
    status: 'active'
  },
  {
    id: '3',
    name: 'Emma Wilson',
    position: 'Payment Coordinator',
    organization: 'Mathematics Society',
    email: 'emma.wilson@university.edu',
    accessLevel: 'Organization Level',
    paymentsProcessed: 89,
    status: 'active'
  },
  {
    id: '4',
    name: 'David Lee',
    position: 'Finance Head',
    organization: 'Student Government',
    email: 'david.lee@university.edu',
    accessLevel: 'University Level',
    paymentsProcessed: 412,
    status: 'active'
  }
];

export function ViewOfficers() {
  const [searchTerm, setSearchTerm] = useState('');
  const [officers] = useState<Officer[]>(mockOfficers);

  const filteredOfficers = officers.filter(
    (officer) =>
      officer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      officer.position.toLowerCase().includes(searchTerm.toLowerCase()) ||
      officer.organization.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusBadge = (status: Officer['status']) => {
    return status === 'active' ? (
      <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full">Active</span>
    ) : (
      <span className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full">Inactive</span>
    );
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-gray-900">Officer Directory</h3>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            Add New Officer
          </button>
        </div>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search by name, position, or organization..."
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
              <th className="px-6 py-3 text-left text-gray-900">Name</th>
              <th className="px-6 py-3 text-left text-gray-900">Position</th>
              <th className="px-6 py-3 text-left text-gray-900">Organization</th>
              <th className="px-6 py-3 text-left text-gray-900">Email</th>
              <th className="px-6 py-3 text-left text-gray-900">Access Level</th>
              <th className="px-6 py-3 text-left text-gray-900">Payments Processed</th>
              <th className="px-6 py-3 text-left text-gray-900">Status</th>
              <th className="px-6 py-3 text-left text-gray-900">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredOfficers.map((officer) => (
              <tr key={officer.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-gray-900">{officer.name}</td>
                <td className="px-6 py-4 text-gray-700">{officer.position}</td>
                <td className="px-6 py-4 text-gray-700">{officer.organization}</td>
                <td className="px-6 py-4 text-gray-700">
                  <div className="flex items-center gap-2">
                    <Mail className="w-4 h-4 text-gray-400" />
                    {officer.email}
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2 text-gray-700">
                    <Shield className="w-4 h-4 text-blue-600" />
                    {officer.accessLevel}
                  </div>
                </td>
                <td className="px-6 py-4 text-gray-900">{officer.paymentsProcessed}</td>
                <td className="px-6 py-4">{getStatusBadge(officer.status)}</td>
                <td className="px-6 py-4">
                  <button className="px-3 py-1 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 transition-colors">
                    Manage
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
