import { useState } from 'react';
import { QRCodeModal } from './QRCodeModal';
import { ReceiptModal } from './ReceiptModal';

interface Fee {
  id: string;
  feeType: string;
  organization: string;
  amount: number;
  status: 'pending' | 'qr-generated' | 'paid';
}

const mockFees: Fee[] = [
  {
    id: '1',
    feeType: 'Membership Fee',
    organization: 'Computer Science Society',
    amount: 500,
    status: 'pending'
  },
  {
    id: '2',
    feeType: 'Event Registration',
    organization: 'Engineering Student Council',
    amount: 350,
    status: 'qr-generated'
  },
  {
    id: '3',
    feeType: 'T-Shirt',
    organization: 'Basketball Team',
    amount: 450,
    status: 'paid'
  },
  {
    id: '4',
    feeType: 'Annual Dues',
    organization: 'Mathematics Society',
    amount: 600,
    status: 'pending'
  }
];

export function OrganizationFeesTable() {
  const [fees, setFees] = useState<Fee[]>(mockFees);
  const [selectedFee, setSelectedFee] = useState<Fee | null>(null);
  const [modalType, setModalType] = useState<'qr' | 'receipt' | null>(null);
  const [ratings, setRatings] = useState<Record<string, number>>({});

  const handleGenerateQR = (fee: Fee) => {
    setFees(fees.map(f => f.id === fee.id ? { ...f, status: 'qr-generated' } : f));
    setSelectedFee({ ...fee, status: 'qr-generated' });
    setModalType('qr');
  };

  const handleViewQR = (fee: Fee) => {
    setSelectedFee(fee);
    setModalType('qr');
  };

  const handleViewReceipt = (fee: Fee) => {
    setSelectedFee(fee);
    setModalType('receipt');
  };

  const handleRating = (feeId: string, rating: number) => {
    setRatings({ ...ratings, [feeId]: rating });
  };

  const getActionButton = (fee: Fee) => {
    if (fee.status === 'pending') {
      return (
        <button
          onClick={() => handleGenerateQR(fee)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Generate QR
        </button>
      );
    } else if (fee.status === 'qr-generated') {
      return (
        <button
          onClick={() => handleViewQR(fee)}
          className="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors"
        >
          View QR
        </button>
      );
    } else {
      return (
        <button
          onClick={() => handleViewReceipt(fee)}
          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        >
          View Receipt
        </button>
      );
    }
  };

  const getStatusBadge = (status: Fee['status']) => {
    const styles = {
      pending: 'bg-yellow-100 text-yellow-800',
      'qr-generated': 'bg-blue-100 text-blue-800',
      paid: 'bg-green-100 text-green-800'
    };

    const labels = {
      pending: 'Pending',
      'qr-generated': 'QR Generated',
      paid: 'Paid'
    };

    return (
      <span className={`px-3 py-1 rounded-full ${styles[status]}`}>
        {labels[status]}
      </span>
    );
  };

  return (
    <>
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-gray-900">Fee Type</th>
                <th className="px-6 py-3 text-left text-gray-900">Organization</th>
                <th className="px-6 py-3 text-left text-gray-900">Amount</th>
                <th className="px-6 py-3 text-left text-gray-900">Status</th>
                <th className="px-6 py-3 text-left text-gray-900">Action</th>
                <th className="px-6 py-3 text-left text-gray-900">Rate QR</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {fees.map((fee) => (
                <tr key={fee.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-gray-900">{fee.feeType}</td>
                  <td className="px-6 py-4 text-gray-700">{fee.organization}</td>
                  <td className="px-6 py-4 text-gray-900">₱{fee.amount.toFixed(2)}</td>
                  <td className="px-6 py-4">{getStatusBadge(fee.status)}</td>
                  <td className="px-6 py-4">{getActionButton(fee)}</td>
                  <td className="px-6 py-4">
                    <div className="flex gap-1">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button
                          key={star}
                          onClick={() => handleRating(fee.id, star)}
                          className={`text-xl ${
                            (ratings[fee.id] || 0) >= star
                              ? 'text-yellow-400'
                              : 'text-gray-300'
                          } hover:text-yellow-400 transition-colors`}
                        >
                          ★
                        </button>
                      ))}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {modalType === 'qr' && selectedFee && (
        <QRCodeModal
          fee={selectedFee}
          onClose={() => {
            setModalType(null);
            setSelectedFee(null);
          }}
        />
      )}

      {modalType === 'receipt' && selectedFee && (
        <ReceiptModal
          fee={selectedFee}
          onClose={() => {
            setModalType(null);
            setSelectedFee(null);
          }}
        />
      )}
    </>
  );
}
