import { Eye } from 'lucide-react';
import { useState } from 'react';
import { ReceiptModal } from './ReceiptModal';

interface Transaction {
  id: string;
  date: string;
  orNumber: string;
  organization: string;
  feeType: string;
  amount: number;
}

const mockTransactions: Transaction[] = [
  {
    id: '1',
    date: '2024-11-20',
    orNumber: 'OR-2024-001234',
    organization: 'Student Council',
    feeType: 'Activity Fee',
    amount: 1200
  },
  {
    id: '2',
    date: '2024-11-18',
    orNumber: 'OR-2024-001189',
    organization: 'Computer Science Society',
    feeType: 'Membership Fee',
    amount: 500
  },
  {
    id: '3',
    date: '2024-11-15',
    orNumber: 'OR-2024-001145',
    organization: 'Engineering Club',
    feeType: 'Event Registration',
    amount: 350
  },
  {
    id: '4',
    date: '2024-11-10',
    orNumber: 'OR-2024-001098',
    organization: 'Sports Committee',
    feeType: 'Equipment Fee',
    amount: 800
  },
  {
    id: '5',
    date: '2024-11-05',
    orNumber: 'OR-2024-001023',
    organization: 'Music Society',
    feeType: 'Annual Dues',
    amount: 600
  }
];

export function TransactionHistoryTable() {
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);

  return (
    <>
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-gray-900">Recent Payment History</h3>
          <p className="text-gray-600">Your completed transactions</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-gray-900">Date</th>
                <th className="px-6 py-3 text-left text-gray-900">OR Number</th>
                <th className="px-6 py-3 text-left text-gray-900">Organization</th>
                <th className="px-6 py-3 text-left text-gray-900">Fee Type</th>
                <th className="px-6 py-3 text-left text-gray-900">Amount</th>
                <th className="px-6 py-3 text-left text-gray-900">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {mockTransactions.map((transaction) => (
                <tr key={transaction.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-gray-900">
                    {new Date(transaction.date).toLocaleDateString('en-US', {
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric'
                    })}
                  </td>
                  <td className="px-6 py-4 text-gray-700">{transaction.orNumber}</td>
                  <td className="px-6 py-4 text-gray-700">{transaction.organization}</td>
                  <td className="px-6 py-4 text-gray-700">{transaction.feeType}</td>
                  <td className="px-6 py-4 text-gray-900">₱{transaction.amount.toFixed(2)}</td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => setSelectedTransaction(transaction)}
                      className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 transition-colors"
                    >
                      <Eye className="w-4 h-4" />
                      View Receipt
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {selectedTransaction && (
        <ReceiptModal
          fee={{
            id: selectedTransaction.id,
            feeType: selectedTransaction.feeType,
            organization: selectedTransaction.organization,
            amount: selectedTransaction.amount,
            status: 'paid'
          }}
          orNumber={selectedTransaction.orNumber}
          date={selectedTransaction.date}
          onClose={() => setSelectedTransaction(null)}
        />
      )}
    </>
  );
}
