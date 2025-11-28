import { useState } from 'react';
import { Camera, CheckCircle, XCircle } from 'lucide-react';

export function QRScanner() {
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<'success' | 'error' | null>(null);
  const [scannedData, setScannedData] = useState<any>(null);

  const handleScan = () => {
    setIsScanning(true);
    // Simulate scanning
    setTimeout(() => {
      const mockData = {
        studentName: 'John Doe',
        studentId: '2023-00456',
        feeType: 'Membership Fee',
        organization: 'Computer Science Society',
        amount: 500
      };
      setScannedData(mockData);
      setScanResult('success');
      setIsScanning(false);
    }, 2000);
  };

  const handleConfirm = () => {
    console.log('Payment confirmed:', scannedData);
    alert('Payment confirmed successfully!');
    setScanResult(null);
    setScannedData(null);
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h3 className="text-gray-900 mb-4">QR Code Scanner</h3>
      
      <div className="space-y-4">
        {/* Scanner Area */}
        <div className="aspect-square max-w-md mx-auto bg-gray-100 rounded-lg flex items-center justify-center relative overflow-hidden">
          {isScanning ? (
            <div className="text-center">
              <Camera className="w-16 h-16 text-gray-400 mx-auto mb-2 animate-pulse" />
              <p className="text-gray-600">Scanning...</p>
            </div>
          ) : scanResult ? (
            <div className="text-center p-6">
              {scanResult === 'success' ? (
                <>
                  <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
                  <p className="text-gray-900 mb-4">QR Code Scanned Successfully</p>
                </>
              ) : (
                <>
                  <XCircle className="w-16 h-16 text-red-600 mx-auto mb-4" />
                  <p className="text-gray-900 mb-4">Invalid QR Code</p>
                </>
              )}
            </div>
          ) : (
            <div className="text-center">
              <Camera className="w-16 h-16 text-gray-400 mx-auto mb-2" />
              <p className="text-gray-600">Ready to scan</p>
            </div>
          )}
        </div>

        {/* Scanned Data */}
        {scannedData && scanResult === 'success' && (
          <div className="bg-gray-50 rounded-lg p-4 space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Student Name</span>
              <span className="text-gray-900">{scannedData.studentName}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Student ID</span>
              <span className="text-gray-900">{scannedData.studentId}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Organization</span>
              <span className="text-gray-900">{scannedData.organization}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Fee Type</span>
              <span className="text-gray-900">{scannedData.feeType}</span>
            </div>
            <div className="flex justify-between border-t border-gray-200 pt-2 mt-2">
              <span className="text-gray-900">Amount</span>
              <span className="text-gray-900">₱{scannedData.amount.toFixed(2)}</span>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          {!scanResult ? (
            <button
              onClick={handleScan}
              disabled={isScanning}
              className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
            >
              {isScanning ? 'Scanning...' : 'Start Scan'}
            </button>
          ) : (
            <>
              <button
                onClick={() => {
                  setScanResult(null);
                  setScannedData(null);
                }}
                className="flex-1 px-4 py-3 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Scan Again
              </button>
              {scanResult === 'success' && (
                <button
                  onClick={handleConfirm}
                  className="flex-1 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  Confirm Payment
                </button>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
