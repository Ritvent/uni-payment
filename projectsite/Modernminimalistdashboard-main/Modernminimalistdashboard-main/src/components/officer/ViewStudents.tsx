import { Search, Eye, Download } from 'lucide-react';
import { useState } from 'react';

interface Student {
  id: string;
  studentId: string;
  name: string;
  program: string;
  year: string;
  email: string;
  totalPaid: number;
  pendingFees: number;
}

const mockStudents: Student[] = [
  {
    id: '1',
    studentId: '2023-00124',
    name: 'Sarah Chen',
    program: 'BS Computer Science',
    year: '3rd Year',
    email: 'sarah.chen@university.edu',
    totalPaid: 2500,
    pendingFees: 500
  },
  {
    id: '2',
    studentId: '2023-00456',
    name: 'John Doe',
    program: 'BS Engineering',
    year: '2nd Year',
    email: 'john.doe@university.edu',
    totalPaid: 1850,
    pendingFees: 350
  },
  {
    id: '3',
    studentId: '2023-00789',
    name: 'Jane Smith',
    program: 'BS Mathematics',
    year: '4th Year',
    email: 'jane.smith@university.edu',
    totalPaid: 3200,
    pendingFees: 0
  },
  {
    id: '4',
    studentId: '2023-00321',
    name: 'Mike Johnson',
    program: 'BS Physics',
    year: '1st Year',
    email: 'mike.johnson@university.edu',
    totalPaid: 1200,
    pendingFees: 800
  }
];

export function ViewStudents() {
  const [searchTerm, setSearchTerm] = useState('');
  const [students] = useState<Student[]>(mockStudents);

  const filteredStudents = students.filter(
    (student) =>
      student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.studentId.includes(searchTerm) ||
      student.program.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="bg-white rounded-lg border border-gray-200">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-gray-900">Student Directory</h3>
          <button className="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors">
            <Download className="w-4 h-4" />
            Export List
          </button>
        </div>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search by name, ID, or program..."
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
              <th className="px-6 py-3 text-left text-gray-900">Student ID</th>
              <th className="px-6 py-3 text-left text-gray-900">Name</th>
              <th className="px-6 py-3 text-left text-gray-900">Program</th>
              <th className="px-6 py-3 text-left text-gray-900">Year Level</th>
              <th className="px-6 py-3 text-left text-gray-900">Email</th>
              <th className="px-6 py-3 text-left text-gray-900">Total Paid</th>
              <th className="px-6 py-3 text-left text-gray-900">Pending Fees</th>
              <th className="px-6 py-3 text-left text-gray-900">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredStudents.map((student) => (
              <tr key={student.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-gray-900">{student.studentId}</td>
                <td className="px-6 py-4 text-gray-700">{student.name}</td>
                <td className="px-6 py-4 text-gray-700">{student.program}</td>
                <td className="px-6 py-4 text-gray-700">{student.year}</td>
                <td className="px-6 py-4 text-gray-700">{student.email}</td>
                <td className="px-6 py-4 text-gray-900">₱{student.totalPaid.toFixed(2)}</td>
                <td className="px-6 py-4">
                  <span className={`${student.pendingFees > 0 ? 'text-red-600' : 'text-green-600'}`}>
                    ₱{student.pendingFees.toFixed(2)}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <button className="flex items-center gap-2 px-3 py-1 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 transition-colors">
                    <Eye className="w-4 h-4" />
                    View Details
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
