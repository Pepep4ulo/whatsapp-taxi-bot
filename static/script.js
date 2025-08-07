// Dashboard functionality for WhatsApp bot

// Initialize feather icons when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    feather.replace();
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(amount);
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Status badge helper
function getStatusBadge(status) {
    const badges = {
        'pending': '<span class="badge bg-warning"><i data-feather="clock"></i> Pendente</span>',
        'confirmed': '<span class="badge bg-success"><i data-feather="check-circle"></i> Confirmada</span>',
        'cancelled': '<span class="badge bg-danger"><i data-feather="x-circle"></i> Cancelada</span>',
        'completed': '<span class="badge bg-info"><i data-feather="check"></i> Concluída</span>'
    };
    
    return badges[status] || `<span class="badge bg-secondary">${status}</span>`;
}

// Real-time updates
function updateDashboard() {
    fetch('/api/rides')
        .then(response => response.json())
        .then(data => {
            // Update ride counts and statistics
            updateStats(data);
            
            // Update recent rides table if on dashboard
            if (document.querySelector('.recent-rides-table')) {
                updateRecentRidesTable(data);
            }
            
            // Update all rides table if on rides page
            if (document.querySelector('.all-rides-table')) {
                updateAllRidesTable(data);
            }
        })
        .catch(error => {
            console.error('Error fetching ride updates:', error);
        });
}

function updateStats(rides) {
    const stats = {
        total: rides.length,
        confirmed: rides.filter(r => r.status === 'confirmed').length,
        pending: rides.filter(r => r.status === 'pending').length,
        cancelled: rides.filter(r => r.status === 'cancelled').length,
        revenue: rides.filter(r => r.status === 'confirmed')
                     .reduce((sum, r) => sum + r.price, 0)
    };
    
    // Update stat cards if they exist
    const totalElement = document.querySelector('.stat-total');
    const confirmedElement = document.querySelector('.stat-confirmed');
    const pendingElement = document.querySelector('.stat-pending');
    const revenueElement = document.querySelector('.stat-revenue');
    
    if (totalElement) totalElement.textContent = stats.total;
    if (confirmedElement) confirmedElement.textContent = stats.confirmed;
    if (pendingElement) pendingElement.textContent = stats.pending;
    if (revenueElement) revenueElement.textContent = formatCurrency(stats.revenue);
}

// Navigation helpers
function navigateToRide(rideId) {
    window.location.href = `/rides#${rideId}`;
}

function openGoogleMaps(origin, destination) {
    const url = `https://www.google.com/maps/dir/${encodeURIComponent(origin)}/${encodeURIComponent(destination)}`;
    window.open(url, '_blank');
}

// Filter functionality for rides page
function initializeFilters() {
    const filterButtons = document.querySelectorAll('input[name="statusFilter"]');
    
    filterButtons.forEach(button => {
        button.addEventListener('change', function() {
            const status = this.id;
            filterRidesByStatus(status);
        });
    });
}

function filterRidesByStatus(status) {
    const rows = document.querySelectorAll('tbody tr[data-status]');
    
    rows.forEach(row => {
        const rowStatus = row.getAttribute('data-status');
        
        if (status === 'all' || rowStatus === status) {
            row.style.display = '';
            row.classList.remove('d-none');
        } else {
            row.style.display = 'none';
            row.classList.add('d-none');
        }
    });
    
    // Update visible count
    const visibleRows = document.querySelectorAll('tbody tr[data-status]:not(.d-none)');
    const countElement = document.querySelector('.rides-count');
    if (countElement) {
        countElement.textContent = `${visibleRows.length} corrida(s)`;
    }
}

// Search functionality
function initializeSearch() {
    const searchInput = document.querySelector('#ridesSearch');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            filterRidesBySearch(searchTerm);
        });
    }
}

function filterRidesBySearch(searchTerm) {
    const rows = document.querySelectorAll('tbody tr[data-status]');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        
        if (text.includes(searchTerm)) {
            row.classList.remove('search-hidden');
        } else {
            row.classList.add('search-hidden');
        }
    });
}

// Notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(notification, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Auto-refresh functionality
let autoRefreshInterval;

function startAutoRefresh(intervalMs = 30000) {
    stopAutoRefresh(); // Clear any existing interval
    
    autoRefreshInterval = setInterval(() => {
        updateDashboard();
    }, intervalMs);
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

// Initialize auto-refresh on page load
document.addEventListener('DOMContentLoaded', function() {
    startAutoRefresh();
    initializeFilters();
    initializeSearch();
});

// Stop auto-refresh when page is hidden
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        stopAutoRefresh();
    } else {
        startAutoRefresh();
    }
});

// Export functions for global access
window.showRideDetails = function(rideId) {
    // Implementation for showing ride details modal
    const modal = new bootstrap.Modal(document.getElementById('rideDetailsModal'));
    
    // Fetch ride details and populate modal
    fetch(`/api/rides/${rideId}`)
        .then(response => response.json())
        .then(ride => {
            const content = document.getElementById('rideDetailsContent');
            content.innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <h6>Informações da Corrida</h6>
                        <table class="table table-sm">
                            <tr><td><strong>ID:</strong></td><td>#${ride.id}</td></tr>
                            <tr><td><strong>Status:</strong></td><td>${getStatusBadge(ride.status)}</td></tr>
                            <tr><td><strong>Data:</strong></td><td>${formatDateTime(ride.created_at)}</td></tr>
                            <tr><td><strong>Cliente:</strong></td><td>${ride.customer_phone}</td></tr>
                            <tr><td><strong>Passageiros:</strong></td><td>${ride.passengers}</td></tr>
                        </table>
                    </div>
                    <div class="col-md-6">
                        <h6>Detalhes da Viagem</h6>
                        <table class="table table-sm">
                            <tr><td><strong>Distância:</strong></td><td>${ride.distance_km.toFixed(1)} km</td></tr>
                            <tr><td><strong>Tempo:</strong></td><td>${ride.duration_minutes} min</td></tr>
                            <tr><td><strong>Valor:</strong></td><td>${formatCurrency(ride.price)}</td></tr>
                        </table>
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-12">
                        <h6>Rota</h6>
                        <div class="mb-2">
                            <strong>Origem:</strong><br>
                            <span class="text-muted">${ride.pickup_location}</span>
                        </div>
                        <div class="mb-3">
                            <strong>Destino:</strong><br>
                            <span class="text-muted">${ride.destination}</span>
                        </div>
                        <button class="btn btn-primary btn-sm" onclick="openGoogleMaps('${ride.pickup_location}', '${ride.destination}')">
                            <i data-feather="navigation"></i> Ver no Google Maps
                        </button>
                    </div>
                </div>
            `;
            
            // Re-initialize feather icons in modal
            feather.replace();
            modal.show();
        })
        .catch(error => {
            console.error('Error fetching ride details:', error);
            showNotification('Erro ao carregar detalhes da corrida', 'danger');
        });
};
