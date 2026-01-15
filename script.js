// Theme toggle functionality
document.addEventListener('DOMContentLoaded', function() {
  const excludedCliPrefixes = ['/blog'];
  const currentPath = window.location.pathname || '/';
  const isExcludedCli = excludedCliPrefixes.some(prefix => currentPath.startsWith(prefix));
  if (!isExcludedCli) {
    document.body.classList.add('cli-theme');
  }

  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = themeToggle.querySelector('i');
  
  // Check for saved theme preference or use preferred color scheme
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.body.classList.add('dark-mode');
    themeIcon.classList.remove('fa-moon');
    themeIcon.classList.add('fa-sun');
  }
  
  // Theme toggle click handler
  themeToggle.addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    
    if (document.body.classList.contains('dark-mode')) {
      localStorage.setItem('theme', 'dark');
      themeIcon.classList.remove('fa-moon');
      themeIcon.classList.add('fa-sun');
    } else {
      localStorage.setItem('theme', 'light');
      themeIcon.classList.remove('fa-sun');
      themeIcon.classList.add('fa-moon');
    }
  });
  
  // Mobile navigation toggle
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  
  navToggle.addEventListener('click', function() {
    navLinks.classList.toggle('active');
    
    // Animate hamburger to X
    const spans = navToggle.querySelectorAll('span');
    if (navLinks.classList.contains('active')) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans[0].style.transform = 'none';
      spans[1].style.opacity = '1';
      spans[2].style.transform = 'none';
    }
  });
  
  // Close mobile menu when clicking on a link
  const navItems = document.querySelectorAll('.nav-links a');
  navItems.forEach(item => {
    item.addEventListener('click', function() {
      if (navLinks.classList.contains('active')) {
        navLinks.classList.remove('active');
        const spans = navToggle.querySelectorAll('span');
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
      }
    });
  });
  
  // Project filtering
  const filterButtons = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');
  
  filterButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Remove active class from all buttons
      filterButtons.forEach(btn => btn.classList.remove('active'));
      
      // Add active class to clicked button
      this.classList.add('active');
      
      // Get filter value
      const filter = this.getAttribute('data-filter');
      
      // Filter projects
      projectCards.forEach(card => {
        if (filter === 'all' || card.getAttribute('data-category') === filter) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
  
  // Citation modal functionality
  const modal = document.getElementById('citeModal');
  const citeBtns = document.querySelectorAll('.js-cite-modal');
  const closeBtn = document.querySelector('.close');
  const citationText = document.getElementById('citationText');
  const copyBtn = document.getElementById('copyCitation');
  
  citeBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const filename = this.getAttribute('data-filename');
      
      // In a real implementation, you would fetch the citation file
      // For this example, we'll use a hardcoded citation
      if (filename.includes('ieice2017')) {
        citationText.textContent = `@article{IEICE2017,
  title={An Improvement of Scalar Multiplication by Skew Frobenius Map with Multi-Scalar Multiplication for KSS Curve},
  author={Md. Al-Amin KHANDAKER and Yasuyuki NOGAMI},
  journal={IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences},
  volume={E100.A},
  number={9},
  pages={1838-1845},
  year={2017},
  doi={10.1587/transfun.E100.A.1838}
}`;
      } else {
        citationText.textContent = `@inproceedings{example,
  title={Example Citation},
  author={Khandaker, Md. Al-Amin},
  booktitle={Example Conference},
  year={2023}
}`;
      }
      
      modal.style.display = 'block';
    });
  });
  
  // Close modal when clicking the × button
  closeBtn.addEventListener('click', function() {
    modal.style.display = 'none';
  });
  
  // Close modal when clicking outside of it
  window.addEventListener('click', function(event) {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });
  
  // Copy citation to clipboard
  copyBtn.addEventListener('click', function() {
    const text = citationText.textContent;
    navigator.clipboard.writeText(text).then(function() {
      copyBtn.textContent = 'Copied!';
      setTimeout(function() {
        copyBtn.textContent = 'Copy to Clipboard';
      }, 2000);
    }, function(err) {
      console.error('Could not copy text: ', err);
    });
  });
  
  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      if (this.getAttribute('href') !== '#') {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          const headerHeight = 70;
          const elementPosition = target.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerHeight;
          
          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
        }
      }
    });
  });
});