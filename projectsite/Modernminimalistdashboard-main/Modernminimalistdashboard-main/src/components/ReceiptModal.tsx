import { X, Download, CheckCircle } from 'lucide-react';

interface ReceiptModalProps {
  fee: {
    id: string;
    feeType: string;
    organization: string;
    amount: number;
  };
  orNumber?: string;
  date?: string;
  onClose: () => void;
}

export function ReceiptModal({ fee, orNumber = 'OR-2024-001234', date, onClose }: ReceiptModalProps) {
  const receiptDate = date || new Date().toISOString().split('T')[0];

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-gray-900">Payment Receipt</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="space-y-6">
          {/* Success Icon */}
          <div className="flex justify-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
              <CheckCircle className="w-10 h-10 text-green-600" />
            </div>
          </div>

          <div className="text-center">
            <p className="text-gray-900 mb-1">Payment Successful</p>
            <p className="text-gray-600">Thank you for your payment</p>
          </div>

          {/* Receipt Details */}
          <div className="border-t border-b border-gray-200 py-4 space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">OR Number</span>
              <span className="text-gray-900">{orNumber}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Date</span>
              <span className="text-gray-900">
                {new Date(receiptDate).toLocaleDateString('en-US', {
                  month: 'long',
                  day: 'numeric',
                  year: 'numeric'
                })}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Organization</span>
              <span className="text-gray-900">{fee.organization}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Fee Type</span>
              <span className="text-gray-900">{fee.feeType}</span>
            </div>
          </div>

          {/* Amount */}
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-900">Total Amount</span>
              <span className="text-gray-900">₱{fee.amount.toFixed(2)}</span>
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <button
              onClick={handlePrint}
              className="flex-1 px-4 py-3 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Print
            </button>
            <button
              onClick={handlePrint}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Download className="w-4 h-4" />
              Download
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
