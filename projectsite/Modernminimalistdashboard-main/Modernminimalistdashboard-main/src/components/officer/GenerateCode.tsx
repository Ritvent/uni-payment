import { useState } from 'react';
import { Copy, Check, Code } from 'lucide-react';

export function GenerateCode() {
  const [copied, setCopied] = useState<string | null>(null);

  const handleCopy = (code: string, type: string) => {
    navigator.clipboard.writeText(code);
    setCopied(type);
    setTimeout(() => setCopied(null), 2000);
  };

  const htmlCode = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>University Payment System</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
    <header>
      <h1>University Payment System</h1>
    </header>
    <main>
      <div class="dashboard">
        <h2>Student Dashboard</h2>
        <div class="card">
          <p>Welcome to the payment portal</p>
        </div>
      </div>
    </main>
  </div>
  <script src="script.js"></script>
</body>
</html>`;

  const cssCode = `* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: system-ui, -apple-system, sans-serif;
  background-color: #f9fafb;
  color: #111827;
  line-height: 1.5;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
}

header {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 1.5rem 0;
  margin-bottom: 2rem;
}

h1 {
  font-size: 1.5rem;
  font-weight: 600;
}

.dashboard {
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
  padding: 2rem;
}

.card {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
}`;

  const jsCode = `// University Payment System JavaScript

document.addEventListener('DOMContentLoaded', function() {
  console.log('University Payment System Loaded');
  
  // Example: Handle form submissions
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      console.log('Form submitted');
    });
  });
  
  // Example: Dynamic content loading
  function loadDashboard() {
    console.log('Loading dashboard...');
    // Add your dashboard logic here
  }
  
  loadDashboard();
});

// Example: Payment processing function
function processPayment(amount, feeType) {
  console.log(\`Processing payment: ₱\${amount} for \${feeType}\`);
  // Add your payment logic here
  return true;
}`;

  const codeBlocks = [
    { title: 'HTML', code: htmlCode, language: 'html', type: 'html' },
    { title: 'CSS', code: cssCode, language: 'css', type: 'css' },
    { title: 'JavaScript', code: jsCode, language: 'javascript', type: 'js' }
  ];

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Code className="w-6 h-6 text-blue-600" />
          <h3 className="text-gray-900">Generate HTML/CSS/JS Code</h3>
        </div>
        <p className="text-gray-600">
          Export starter code templates for the university payment system. These templates can be customized for your specific needs.
        </p>
      </div>

      {codeBlocks.map((block) => (
        <div key={block.type} className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-gray-50">
            <h4 className="text-gray-900">{block.title}</h4>
            <button
              onClick={() => handleCopy(block.code, block.type)}
              className="flex items-center gap-2 px-3 py-1 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors"
            >
              {copied === block.type ? (
                <>
                  <Check className="w-4 h-4" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  Copy Code
                </>
              )}
            </button>
          </div>
          <div className="p-4 bg-gray-900 overflow-x-auto">
            <pre className="text-gray-100">
              <code>{block.code}</code>
            </pre>
          </div>
        </div>
      ))}

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-blue-900">
          <strong>Note:</strong> These are starter templates. Customize them according to your specific requirements and integrate with your backend system for full functionality.
        </p>
      </div>
    </div>
  );
}
