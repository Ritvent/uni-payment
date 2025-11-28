import { X, Download } from 'lucide-react';

interface QRCodeModalProps {
  fee: {
    id: string;
    feeType: string;
    organization: string;
    amount: number;
  };
  onClose: () => void;
}

export function QRCodeModal({ fee, onClose }: QRCodeModalProps) {
  const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(
    JSON.stringify({
      feeId: fee.id,
      feeType: fee.feeType,
      organization: fee.organization,
      amount: fee.amount
    })
  )}`;

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = qrCodeUrl;
    link.download = `qr-${fee.id}.png`;
    link.click();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-gray-900">Payment QR Code</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="space-y-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-gray-600">Organization</p>
            <p className="text-gray-900">{fee.organization}</p>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-gray-600">Fee Type</p>
            <p className="text-gray-900">{fee.feeType}</p>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-gray-600">Amount</p>
            <p className="text-gray-900">₱{fee.amount.toFixed(2)}</p>
          </div>

          <div className="flex justify-center py-6">
            <img
              src={qrCodeUrl}
              alt="Payment QR Code"
              className="w-64 h-64 border-4 border-gray-200 rounded-lg"
            />
          </div>

          <p className="text-center text-gray-600">
            Scan this QR code to complete your payment
          </p>

          <button
            onClick={handleDownload}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Download className="w-4 h-4" />
            Download QR Code
          </button>
        </div>
      </div>
    </div>
  );
}
